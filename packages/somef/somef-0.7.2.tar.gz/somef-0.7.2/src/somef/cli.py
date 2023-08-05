# creatJSON.py
# parameters:
## input file: either: url to github repository OR markdown documentation file path
## output file: json with each excerpt marked with all four classification scores

import argparse
import base64
import json
import os
import pickle
import re
import sys
import tempfile
import time
import urllib
from datetime import datetime

import markdown
import validators
import zipfile
from io import StringIO
from os import path
from pathlib import Path
from urllib.parse import urlparse

import requests
from dateutil import parser as date_parser
from markdown import Markdown

from somef.data_to_graph import DataGraph
from . import createExcerpts
from . import header_analysis

from . import parser_somef


## Markdown to plain text conversion: begin ##
# code snippet from https://stackoverflow.com/a/54923798
def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# patching Markdown
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    return __md.convert(text)


## Markdown to plain text conversion: end ##

def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError(f"{x} not in range [0.0, 1.0]")
    return x


categories = ['description', 'citation', 'installation', 'invocation']
# keep_keys = ('description', 'name', 'owner', 'license', 'languages_url', 'forks_url')
# instead of keep keys, we have this table
# it says that we want the key "codeRepository", and that we'll get it from the path "html_url" within the result object
github_crosswalk_table = {
    "codeRepository": "html_url",
    "languages_url": "languages_url",
    "owner": ["owner", "login"],
    "ownerType": ["owner", "type"],  # used to determine if owner is User or Organization
    "dateCreated": "created_at",
    "dateModified": "updated_at",
    "license": "license",
    "description": "description",
    "name": "name",
    "fullName": "full_name",
    "issueTracker": "issues_url",
    "forksUrl": "forks_url",
    "stargazers_count": "stargazers_count",
    "forks_count": "forks_count"
}

release_crosswalk_table = {
    'tagName': 'tag_name',
    'name': 'name',
    'authorName': ['author', 'login'],
    'authorType': ['author', 'type'],
    'body': 'body',
    'tarballUrl': 'tarball_url',
    'zipballUrl': 'zipball_url',
    'htmlUrl': 'html_url',
    'url': 'url',
    'dateCreated': 'created_at',
    'datePublished': "published_at",
}


# the same as requests.get(args).json(), but protects against rate limiting
def rate_limit_get(*args, backoff_rate=2, initial_backoff=1, **kwargs):
    rate_limited = True
    response = {}
    date = ""
    while rate_limited:
        response = requests.get(*args, **kwargs)
        data = response
        date = data.headers["date"]
        rate_limit_remaining = data.headers["x-ratelimit-remaining"]
        epochtime = int(data.headers["x-ratelimit-reset"])
        date_reset = datetime.fromtimestamp(epochtime)
        print("Rate limit ramaining: " + rate_limit_remaining + " ### Next rate limit reset at: " + str(date_reset))
        response = response.json()
        if 'message' in response and 'API rate limit exceeded' in response['message']:
            rate_limited = True
            print(f"rate limited. Backing off for {initial_backoff} seconds")
            time.sleep(initial_backoff)

            # increase the backoff for next time
            initial_backoff *= backoff_rate
        else:
            rate_limited = False

    return response, date


# error when github url is wrong
class GithubUrlError(Exception):
    # print("The URL provided seems to be incorrect")
    pass


def load_repository_metadata(repository_url, header):
    """
    Function uses the repository_url provided to load required information from github.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    repository_url
    header

    Returns
    -------
    Returns the readme text and required metadata
    """
    if repository_url.rfind("gitlab.com") > 0:
        return load_repository_metadata_gitlab(repository_url, header)

    print(f"Loading Repository {repository_url} Information....")
    ## load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    if url.netloc != 'github.com':
        print("Error: repository must come from github")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        print("Repository link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]

    repo_api_base_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    repo_ref = None
    ref_param = None

    if len(path_components) >= 5:
        if not path_components[3] == "tree":
            print(
                "Github link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}/tree/{ref}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        repo_ref = "/".join(path_components[4:])
        ref_param = {"ref": repo_ref}

    print(repo_api_base_url)

    general_resp, date = rate_limit_get(repo_api_base_url, headers=header)

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: Repository name is private or incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if repo_ref is None:
        repo_ref = general_resp['default_branch']

    ## get only the fields that we want
    def do_crosswalk(data, crosswalk_table):
        def get_path(obj, path):
            if isinstance(path, list) or isinstance(path, tuple):
                if len(path) == 1:
                    path = path[0]
                else:
                    return get_path(obj[path[0]], path[1:])

            if obj is not None and path in obj:
                return obj[path]
            else:
                return None

        output = {}
        for codemeta_key, path in crosswalk_table.items():
            value = get_path(data, path)
            if value is not None:
                output[codemeta_key] = value
            else:
                print(f"Error: key {path} not present in github repository")
        return output

    filtered_resp = do_crosswalk(general_resp, github_crosswalk_table)
    # add download URL
    filtered_resp["downloadUrl"] = f"https://github.com/{owner}/{repo_name}/releases"

    ## condense license information
    license_info = {}
    if 'license' in filtered_resp:
        for k in ('name', 'url'):
            if k in filtered_resp['license']:
                license_info[k] = filtered_resp['license'][k]

    ## If we didn't find it, look for the license
    if 'url' not in license_info or license_info['url'] is None:

        possible_license_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/LICENSE"
        license_text_resp = requests.get(possible_license_url)

        # todo: It's possible that this request will get rate limited. Figure out how to detect that.
        if license_text_resp.status_code == 200:
            # license_text = license_text_resp.text
            license_info['url'] = possible_license_url

    if len(license_info) > 0:
        filtered_resp['license'] = license_info

    topics_headers = header
    # get keywords / topics
    if 'topics' in general_resp.keys():
        filtered_resp['topics'] = general_resp['topics']
    #else:
    #    topics_headers = header
    #    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    #    topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
    #                                       headers=topics_headers)

    #    if 'message' in topics_resp.keys():
    #        print("Topics Error: " + topics_resp['message'])
    #    elif topics_resp and 'names' in topics_resp.keys():
    #        filtered_resp['topics'] = topics_resp['names']

    # get social features: stargazers_count
    stargazers_info = {}
    if 'stargazers_count' in filtered_resp:
        stargazers_info['count'] = filtered_resp['stargazers_count']
        stargazers_info['date'] = date
        del filtered_resp['stargazers_count']
    filtered_resp['stargazersCount'] = stargazers_info

    # get social features: forks_count
    forks_info = {}
    if 'forks_count' in filtered_resp:
        forks_info['count'] = filtered_resp['forks_count']
        forks_info['date'] = date
        del filtered_resp['forks_count']
    filtered_resp['forksCount'] = forks_info

    ## get languages
    languages, date = rate_limit_get(filtered_resp['languages_url'], headers=header)
    if "message" in languages:
        print("Languages Error: " + languages["message"])
    else:
        filtered_resp['languages'] = list(languages.keys())

    del filtered_resp['languages_url']

    # get default README
    #                                   headers=topics_headers,
    #readme_info, date = rate_limit_get(repo_api_base_url + "/readme",
    #                                   headers=topics_headers,
    #                                   params=ref_param)
    #if 'message' in readme_info.keys():
    #    print("README Error: " + readme_info['message'])
    #    text = ""
    #else:
    #    readme = base64.b64decode(readme_info['content']).decode("utf-8")
    #    text = readme
    #    filtered_resp['readmeUrl'] = readme_info['html_url']

    # get full git repository
    # todo: maybe it should be optional, as this could take some time?

    text = ""
    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # download the repo at the selected branch with the link
        repo_archive_url = f"https://github.com/{owner}/{repo_name}/archive/{repo_ref}.zip"
        print(f"Downloading {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)
        if repo_download.status_code != 200:
            sys.exit(f"Error: Archive request failed with HTTP {repo_download.status_code}")
        repo_zip = repo_download.content

        repo_zip_file = os.path.join(temp_dir, "repo.zip")
        repo_extract_dir = os.path.join(temp_dir, "repo")

        with open(repo_zip_file, "wb") as f:
            f.write(repo_zip)

        with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
            zip_ref.extractall(repo_extract_dir)

        repo_folders = os.listdir(repo_extract_dir)
        assert (len(repo_folders) == 1)

        repo_dir = os.path.join(repo_extract_dir, repo_folders[0])

        notebooks = []
        dockerfiles = []
        docs = []
        scriptfiles = []

        for dirpath, dirnames, filenames in os.walk(repo_dir):
            repo_relative_path = os.path.relpath(dirpath, repo_dir)
            for filename in filenames:
                if filename == "Dockerfile":
                    # dockerfiles.append(os.path.join(repo_relative_path, filename))
                    dockerfiles.append(repo_relative_path + "/" + filename)
                if filename.lower().endswith(".ipynb"):
                    notebooks.append(os.path.join(repo_relative_path, filename))
                if "README" == filename.upper() or "README.MD" == filename.upper():
                    if (repo_relative_path == "."):
                        try:
                            with open(os.path.join(dirpath, filename), "rb") as data_file:
                                data_file_text = data_file.read()
                                text = data_file_text.decode("utf-8")
                                if repository_url.endswith("/"):
                                    filtered_resp['readmeUrl'] = repository_url + filename
                                else:
                                    filtered_resp['readmeUrl'] = repository_url + "/" + filename
                        except:
                            print("README Error: error while reading file content")

                if "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "rb") as data_file:
                            file_text = data_file.read()
                            filtered_resp["licenseText"] = unmark(file_text)
                    except:
                        # TO DO: try different encodings
                        filtered_resp["licenseFile"] = convert_to_raw_usercontent(filename, owner, repo_name, repo_ref)

                if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                    filtered_resp["codeOfConduct"] = convert_to_raw_usercontent(filename, owner, repo_name, repo_ref)
                if "CONTRIBUTING" == filename.upper() or "CONTRIBUTING.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["contributingGuidelines"] = unmark(file_text)
                    except:
                        filtered_resp["contributingGuidelinesFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                                 repo_name,
                                                                                                 repo_ref)
                if "ACKNOWLEDGMENT" in filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["acknowledgments"] = unmark(file_text)
                    except:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                          repo_name,
                                                                                          repo_ref)
                if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["contributors"] = unmark(file_text)
                    except:
                        filtered_resp["contributorsFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                       repo_name,
                                                                                       repo_ref)
                if "CITATION" == filename.upper() or "CITATION.CFF" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["citation"] = unmark(file_text)
                    except:
                        filtered_resp["citationFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                   repo_name,
                                                                                   repo_ref)
                if filename.endswith(".sh"):
                    # scriptfiles.append(os.path.join(repo_relative_path, filename))
                    scriptfiles.append(repo_relative_path + "/" + filename)

            for dirname in dirnames:
                if dirname.lower() == "docs":
                    if repo_relative_path == ".":
                        docs_path = dirname
                    else:
                        docs_path = repo_relative_path + "/" + dirname
                    docs.append(
                        f"https://github.com/{owner}/{repo_name}/tree/{urllib.parse.quote(repo_ref)}/{docs_path}")
                    # print(docs)

        # print("NOTEBOOKS:")
        # print(notebooks)

        # print("DOCKERFILES:")
        # print(dockerfiles)

    if len(notebooks) > 0:
        filtered_resp["hasExecutableNotebook"] = [convert_to_raw_usercontent(x, owner, repo_name, repo_ref) for x in
                                                  notebooks]
    if len(dockerfiles) > 0:
        filtered_resp["hasBuildFile"] = [convert_to_raw_usercontent(x, owner, repo_name, repo_ref) for x in dockerfiles]
    if len(docs) > 0:
        filtered_resp["hasDocumentation"] = docs

    if len(scriptfiles) > 0:
        filtered_resp["hasScriptFile"] = [convert_to_raw_usercontent(x, owner, repo_name, repo_ref) for x in
                                          scriptfiles]

    # get releases
    releases_list, date = rate_limit_get(repo_api_base_url + "/releases",
                                         headers=header)

    if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        print("Releases Error: " + releases_list['message'])
    else:
        filtered_resp['releases'] = [do_crosswalk(release, release_crosswalk_table) for release in releases_list]

    print("Repository Information Successfully Loaded. \n")
    return text, filtered_resp


def load_repository_metadata_gitlab(repository_url, header):
    """
    Function uses the repository_url provided to load required information from github.
    Information kept from the repository is written in keep_keys.
    Parameters
    ----------
    repository_url
    header

    Returns
    -------
    Returns the readme text and required metadata
    """
    print(f"Loading Repository {repository_url} Information....")
    ## load general response of the repository
    if repository_url[-1] == '/':
        repository_url = repository_url[:-1]
    url = urlparse(repository_url)
    if url.netloc != 'gitlab.com':
        print("Error: repository must come from github")
        return " ", {}

    path_components = url.path.split('/')

    if len(path_components) < 3:
        print("Gitlab link is not correct. \nThe correct format is https://github.com/{owner}/{repo_name}.")
        return " ", {}

    owner = path_components[1]
    repo_name = path_components[2]
    if len(path_components) == 4:
        repo_name = repo_name + '/' + path_components[3]

    project_id = get_project_id(repository_url)
    project_api_url = f"https://gitlab.com/api/v4/projects/{project_id}"
    print(f"Downloading {project_api_url}")
    details = requests.get(project_api_url)
    project_details = details.json()
    date = details.headers["date"]

    repo_api_base_url = f"{repository_url}"

    repo_ref = None
    ref_param = None

    if len(path_components) >= 5:
        if not path_components[4] == "tree":
            print(
                "GitLab link is not correct. \nThe correct format is https://gitlab.com/{owner}/{repo_name}.")

            return " ", {}

        # we must join all after 4, as sometimes tags have "/" in them.
        repo_ref = "/".join(path_components[5:])
        ref_param = {"ref": repo_ref}

    print(repo_api_base_url)
    if 'defaultBranch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['defaultBranch']}
    elif 'default_branch' in project_details.keys():
        general_resp = {'defaultBranch': project_details['default_branch']}

    if 'message' in general_resp:
        if general_resp['message'] == "Not Found":
            print("Error: repository name is incorrect")
        else:
            message = general_resp['message']
            print("Error: " + message)

        raise GithubUrlError

    if repo_ref is None:
        repo_ref = general_resp['defaultBranch']

    ## get only the fields that we want
    def do_crosswalk(data, crosswalk_table):
        def get_path(obj, path):
            if isinstance(path, list) or isinstance(path, tuple):
                if len(path) == 1:
                    path = path[0]
                else:
                    return get_path(obj[path[0]], path[1:])

            if obj is not None and path in obj:
                return obj[path]
            else:
                return None

        output = {}
        for codemeta_key, path in crosswalk_table.items():
            value = get_path(data, path)
            if value is not None:
                output[codemeta_key] = value
            else:
                print(f"Error: key {path} not present in gitlab repository")
        return output

    # filtered_resp = do_crosswalk(general_resp, github_crosswalk_table)
    filtered_resp = {}
    # add download URL
    # filtered_resp["downloadUrl"] = f"https://github.com/{owner}/{repo_name}/releases"
    filtered_resp["downloadUrl"] = f"https://gitlab.com/{owner}/{repo_name}/-/branches"

    ## condense license information
    license_info = {}
    if 'license' in filtered_resp:
        for k in ('name', 'url'):
            if k in filtered_resp['license']:
                license_info[k] = filtered_resp['license'][k]

    ## If we didn't find it, look for the license
    if 'url' not in license_info or license_info['url'] is None:

        possible_license_url = f"{repository_url}/-/blob/master/LICENSE"
        license_text_resp = requests.get(possible_license_url)

        # todo: It's possible that this request will get rate limited. Figure out how to detect that.
        if license_text_resp.status_code == 200:
            # license_text = license_text_resp.text
            license_info['url'] = possible_license_url

    if license_info != '':
        filtered_resp['license'] = license_info

    # get keywords / topics
    topics_headers = header
    topics_headers['accept'] = 'application/vnd.github.mercy-preview+json'
    # topics_resp, date = rate_limit_get(repo_api_base_url + "/topics",
    #                                   headers=topics_headers)
    topics_resp = {}

    if 'message' in topics_resp.keys():
        print("Topics Error: " + topics_resp['message'])
    elif topics_resp and 'names' in topics_resp.keys():
        filtered_resp['topics'] = topics_resp['names']

    if project_details['topics'] is not None:
        filtered_resp['topics'] = project_details['topics']

    # get social features: stargazers_count
    stargazers_info = {}
    # if 'stargazers_count' in filtered_resp:
    if project_details['star_count'] is not None:
        stargazers_info['count'] = project_details['star_count']
        stargazers_info['date'] = date
        if 'stargazers_count' in filtered_resp.keys():
            del filtered_resp['stargazers_count']
    filtered_resp['stargazersCount'] = stargazers_info

    # get social features: forks_count
    forks_info = {}
    # if 'forks_count' in filtered_resp:
    if project_details['forks_count'] is not None:
        forks_info['count'] = project_details['forks_count']
        forks_info['date'] = date
        if 'forks_count' in filtered_resp.keys():
            del filtered_resp['forks_count']
    filtered_resp['forksCount'] = forks_info

    ## get languages
    # languages, date = rate_limit_get(filtered_resp['languages_url'])
    languages = {}
    filtered_resp['languages_url'] = "languages_url"
    if "message" in languages:
        print("Languages Error: " + languages["message"])
    else:
        filtered_resp['languages'] = list(languages.keys())

    del filtered_resp['languages_url']

    # get default README
    # repo_api_base_url https://api.github.com/dgarijo/Widoco/readme
    # readme_info, date = rate_limit_get(repo_api_base_url + "/readme",
    #                                   headers=topics_headers,
    #                                   params=ref_param)
    readme_info = {}
    if 'message' in readme_info.keys():
        print("README Error: " + readme_info['message'])
        text = ""
    elif 'content' in readme_info:
        readme = base64.b64decode(readme_info['content']).decode("utf-8")
        text = readme
        filtered_resp['readmeUrl'] = readme_info['html_url']

    if 'readme_url' in project_details:
        text = get_readme_content(project_details['readme_url'])
        filtered_resp['readmeUrl'] = project_details['readme_url']

    # get full git repository
    # todo: maybe it should be optional, as this could take some time?

    # create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:

        # download the repo at the selected branch with the link
        # https://gitlab.com/unboundedsystems/adapt/-/archive/master/adapt-master.zip
        repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_ref}/{repo_name}-{repo_ref}.zip"
        if len(path_components) == 4:
            repo_archive_url = f"https://gitlab.com/{owner}/{repo_name}/-/archive/{repo_ref}/{path_components[3]}.zip"
        print(f"Downloading {repo_archive_url}")
        repo_download = requests.get(repo_archive_url)
        repo_zip = repo_download.content

        repo_zip_file = os.path.join(temp_dir, "repo.zip")
        repo_extract_dir = os.path.join(temp_dir, "repo")

        with open(repo_zip_file, "wb") as f:
            f.write(repo_zip)

        with zipfile.ZipFile(repo_zip_file, "r") as zip_ref:
            zip_ref.extractall(repo_extract_dir)

        repo_folders = os.listdir(repo_extract_dir)
        assert (len(repo_folders) == 1)

        repo_dir = os.path.join(repo_extract_dir, repo_folders[0])

        notebooks = []
        dockerfiles = []
        docs = []
        scriptfiles = []

        for dirpath, dirnames, filenames in os.walk(repo_dir):
            repo_relative_path = os.path.relpath(dirpath, repo_dir)
            for filename in filenames:
                if filename == "Dockerfile":
                    # dockerfiles.append(os.path.join(repo_relative_path, filename))
                    dockerfiles.append(repo_relative_path + "/" + filename)
                if filename.lower().endswith(".ipynb"):
                    notebooks.append(os.path.join(repo_relative_path, filename))
                if "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "rb") as data_file:
                            file_text = data_file.read()
                            filtered_resp["licenseText"] = unmark(file_text)
                    except:
                        # TO DO: try different encodings
                        filtered_resp["licenseFile"] = convert_to_raw_usercontent(filename, owner, repo_name, repo_ref)

                if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                    filtered_resp["codeOfConduct"] = convert_to_raw_usercontent(filename, owner, repo_name, repo_ref)
                if "CONTRIBUTING" == filename.upper() or "CONTRIBUTING.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["contributingGuidelines"] = unmark(file_text)
                    except:
                        filtered_resp["contributingGuidelinesFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                                 repo_name,
                                                                                                 repo_ref)
                if "ACKNOWLEDGMENT" in filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["acknowledgments"] = unmark(file_text)
                    except:
                        filtered_resp["acknowledgmentsFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                          repo_name,
                                                                                          repo_ref)
                if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["contributors"] = unmark(file_text)
                    except:
                        filtered_resp["contributorsFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                       repo_name,
                                                                                       repo_ref)
                if "CITATION" == filename.upper() or "CITATION.CFF" == filename.upper():
                    try:
                        with open(os.path.join(dirpath, filename), "r") as data_file:
                            file_text = data_file.read()
                            filtered_resp["citation"] = unmark(file_text)
                    except:
                        filtered_resp["citationFile"] = convert_to_raw_usercontent(filename, owner,
                                                                                   repo_name,
                                                                                   repo_ref)
                if filename.endswith(".sh"):
                    # scriptfiles.append(os.path.join(repo_relative_path, filename))
                    scriptfiles.append(repo_relative_path + "/" + filename)

            for dirname in dirnames:
                if dirname.lower() == "docs":
                    if repo_relative_path == ".":
                        docs_path = dirname
                    else:
                        docs_path = repo_relative_path + "/" + dirname
                    docs.append(
                        f"https://gitlab.com/{owner}/{repo_name}/-/tree/{urllib.parse.quote(repo_ref)}/{docs_path}")
                    # print(docs)

        # print("NOTEBOOKS:")
        # print(notebooks)

        # print("DOCKERFILES:")
        # print(dockerfiles)

    if len(notebooks) > 0:
        filtered_resp["hasExecutableNotebook"] = [convert_to_raw_usercontent_gitlab(x, owner, repo_name, repo_ref) for x
                                                  in
                                                  notebooks]
    if len(dockerfiles) > 0:
        filtered_resp["hasBuildFile"] = [convert_to_raw_usercontent_gitlab(x, owner, repo_name, repo_ref) for x in
                                         dockerfiles]
    if len(docs) > 0:
        filtered_resp["hasDocumentation"] = docs

    if len(scriptfiles) > 0:
        filtered_resp["hasScriptFile"] = [convert_to_raw_usercontent_gitlab(x, owner, repo_name, repo_ref) for x in
                                          scriptfiles]

    # get releases
    # releases_list, date = rate_limit_get(repo_api_base_url + "/-/releases",
    #                                     headers=header)

    releases_list = {}
    if isinstance(releases_list, dict) and 'message' in releases_list.keys():
        print("Releases Error: " + releases_list['message'])
    else:
        filtered_resp['releases'] = [do_crosswalk(release, release_crosswalk_table) for release in releases_list]

    print("Repository Information Successfully Loaded. \n")
    return text, filtered_resp


def get_project_id(repository_url):
    print(f"Downloading {repository_url}")
    response = requests.get(repository_url)
    response_str = str(response.content.decode('utf-8'))
    init = response_str.find('\"project_id\":')
    project_id = "-1"
    start = init + len("\"project_id\":")
    if init >= 0:
        end = 0
        end_bracket = response_str.find("}", start)
        comma = response_str.find(",", start)
        if comma != -1 and comma < end_bracket:
            end = comma
        else:
            end = end_bracket
        if end >= 0:
            project_id = response_str[start:end]
    return project_id


def load_local_repository_metadata(local_repo):
    filtered_resp = {}
    notebooks = []
    dockerfiles = []
    docs = []
    scriptfiles = []
    text = ""
    repo_dir = os.path.abspath(local_repo)
    if os.path.exists(os.path.join(repo_dir, "README")):
        with open(os.path.join(os.path.join(repo_dir, "README")), "r", encoding='utf-8') as data_file:
            text = data_file.read()
    elif os.path.exists(os.path.join(repo_dir, "README.MD")):
        with open(os.path.join(os.path.join(repo_dir, "README.MD")), "r", encoding='utf-8') as data_file:
            text = data_file.read()
    elif os.path.exists(os.path.join(repo_dir, "README.md")):
        with open(os.path.join(os.path.join(repo_dir, "README.md")), "r", encoding='utf-8') as data_file:
            text = data_file.read()
    for dirpath, dirnames, filenames in os.walk(repo_dir):
        repo_relative_path = os.path.relpath(dirpath, repo_dir)
        for filename in filenames:
            if filename == "Dockerfile":
                dockerfiles.append(os.path.join(repo_dir, repo_relative_path, filename))
            if filename.lower().endswith(".ipynb"):
                notebooks.append(os.path.join(repo_dir, repo_relative_path, filename))
            if "LICENSE" == filename.upper() or "LICENSE.MD" == filename.upper():
                try:
                    with open(os.path.join(dirpath, filename), "rb") as data_file:
                        file_text = data_file.read()
                        filtered_resp["licenseText"] = unmark(file_text)
                except:
                    filtered_resp["licenseFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CODE_OF_CONDUCT" == filename.upper() or "CODE_OF_CONDUCT.MD" == filename.upper():
                filtered_resp["codeOfConduct"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CONTRIBUTING" == filename.upper() or "CONTRIBUTING.MD" == filename.upper():
                try:
                    with open(os.path.join(dirpath, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["contributingGuidelines"] = unmark(file_text)
                except:
                    filtered_resp["contributingGuidelinesFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "ACKNOWLEDGMENT" in filename.upper():
                try:
                    with open(os.path.join(dirpath, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["acknowledgments"] = unmark(file_text)
                except:
                    filtered_resp["acknowledgmentsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CONTRIBUTORS" == filename.upper() or "CONTRIBUTORS.MD" == filename.upper():
                try:
                    with open(os.path.join(dirpath, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["contributors"] = unmark(file_text)
                except:
                    filtered_resp["contributorsFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if "CITATION" == filename.upper() or "CITATION.CFF" == filename.upper():
                try:
                    with open(os.path.join(dirpath, filename), "r") as data_file:
                        file_text = data_file.read()
                        filtered_resp["citation"] = unmark(file_text)
                except:
                    filtered_resp["citationFile"] = os.path.join(repo_dir, repo_relative_path, filename)
            if filename.endswith(".sh"):
                scriptfiles.append(os.path.join(repo_dir, repo_relative_path, filename))

        for dirname in dirnames:
            if dirname.lower() == "docs":
                if repo_relative_path == ".":
                    docs_path = dirname
                else:
                    docs_path = os.path.join(repo_relative_path, dirname)
                docs.append(os.path.join(repo_dir,docs_path))

    if len(notebooks) > 0:
        filtered_resp["hasExecutableNotebook"] = notebooks
    if len(dockerfiles) > 0:
        filtered_resp["hasBuildFile"] = dockerfiles
    if len(docs) > 0:
        filtered_resp["hasDocumentation"] = docs

    if len(scriptfiles) > 0:
        filtered_resp["hasScriptFile"] = scriptfiles

    print("Local Repository Information Successfully Loaded. \n")
    return text, filtered_resp



def get_readme_content(readme_url):
    readme_url = readme_url.replace("/blob/", "/raw/")
    readme = requests.get(readme_url)
    readme_text = readme.content.decode('utf-8')
    return readme_text


def convert_to_raw_usercontent(partial, owner, repo_name, repo_ref):
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    return f"https://raw.githubusercontent.com/{owner}/{repo_name}/{repo_ref}/{urllib.parse.quote(partial)}"


def convert_to_raw_usercontent_gitlab(partial, owner, repo_name, repo_ref):
    if partial.startswith("./"):
        partial = partial.replace("./", "")
    if partial.startswith(".\\"):
        partial = partial.replace(".\\", "")
    return f"https://gitlab.com/{owner}/{repo_name}/-/blob/{repo_ref}/{urllib.parse.quote(partial)}"


def remove_bibtex(string_list):
    """
        Function that takes the string list and removes all bibtex blocks of it
        Parameters
        ----------
        string_list A list of strings

        Returns
        -------
        The strings list without bibtex blocks
        """
    for x, element in enumerate(string_list):
        bib_references = extract_bibtex(element)
        if len(bib_references) > 0:
            top = element.find(bib_references[0])
            init = element.rfind("```", 0, top)
            end = element.find("```", init + 3)
            substring = element[init:end + 3]
            string_list[x] = element.replace(substring, "")
    return string_list


## Function takes readme text as input and divides it into excerpts
## Returns the extracted excerpts
def create_excerpts(string_list):
    print("Splitting text into valid excerpts for classification")
    string_list = remove_bibtex(string_list)
    # divisions = createExcerpts.split_into_excerpts(string_list)
    divisions = parser_somef.extract_blocks_excerpts(string_list)
    print("Text Successfully split. \n")
    return divisions


def run_classifiers(excerpts, file_paths):
    """
    Function takes readme text as input and runs the provided classifiers on it
    Returns the dictionary containing scores for each excerpt.
    Parameters
    ----------
    excerpts text fragments to process
    file_paths pickle files of the classifiers

    Returns
    -------

    """
    score_dict = {}
    if len(excerpts) > 0:
        for category in categories:
            if category not in file_paths.keys():
                sys.exit("Error: Category " + category + " file path not present in config.json")
            file_name = file_paths[category]
            if not path.exists(file_name):
                sys.exit(f"Error: File/Directory {file_name} does not exist")
            print("Classifying excerpts for the category", category)
            classifier = pickle.load(open(file_name, 'rb'))
            scores = classifier.predict_proba(excerpts)
            score_dict[category] = {'excerpt': excerpts, 'confidence': scores[:, 1]}
            print("Excerpt Classification Successful for the Category", category)
        print("\n")

    return score_dict


def remove_unimportant_excerpts(excerpt_element):
    """
    Function which removes all excerpt lines which have been classified but contain only one word.
    Parameters
    ----------
    excerpt_element

    Returns
    -------
    Returns the excerpt to be entered into the predictions
    """
    excerpt_info = excerpt_element['excerpt']
    excerpt_confidence = excerpt_element['confidence']
    if 'originalHeader' in excerpt_element:
        final_excerpt = {'excerpt': "", 'confidence': [], 'technique': 'Supervised classification',
                         'originalHeader': ""}
    else:
        final_excerpt = {'excerpt': "", 'confidence': [], 'technique': 'Supervised classification'}
    final_excerpt['excerpt'] += excerpt_info;
    final_excerpt['confidence'].append(excerpt_confidence)
    if 'originalHeader' in excerpt_element:
        final_excerpt['originalHeader'] += excerpt_element['originalHeader']
    if 'parentHeader' in excerpt_element and excerpt_element['parentHeader'] != "":
        final_excerpt['parentHeader'] = excerpt_element['parentHeader']
    return final_excerpt


## Function takes scores dictionary and a threshold as input
## Returns predictions containing excerpts with a confidence above the given threshold.
def classify(scores, threshold, excerpts_headers, header_parents):
    print("Checking Thresholds for Classified Excerpts.")
    predictions = {}
    for ele in scores.keys():
        print("Running for", ele)
        flag = False
        predictions[ele] = []
        excerpt = ""
        confid = []
        header = ""
        for i in range(len(scores[ele]['confidence'])):
            if scores[ele]['confidence'][i] >= threshold:
                element = scores[ele]['excerpt'][i]
                if element in set(excerpts_headers['text']):
                    elem = excerpts_headers.loc[excerpts_headers['text'] == element]
                    ind = elem.index.values[0]
                    header = elem.at[ind, 'header']
                if flag == False:
                    excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                    confid.append(scores[ele]['confidence'][i])
                    flag = True
                else:
                    excerpt = excerpt + scores[ele]['excerpt'][i] + ' \n'
                    confid.append(scores[ele]['confidence'][i])
            else:
                if flag == True:
                    if not header == "":
                        element = remove_unimportant_excerpts(
                            {'excerpt': excerpt, 'confidence': confid, 'originalHeader': header,
                             'parentHeader': header_parents[header]})
                        header == ""
                    else:
                        element = remove_unimportant_excerpts({'excerpt': excerpt, 'confidence': confid})
                    if len(element['confidence']) != 0:
                        predictions[ele].append(element)
                    excerpt = ""
                    confid = []
                    flag = False
        print("Run completed.")
    print("All Excerpts below the given Threshold Removed. \n")
    return predictions


def extract_categories_using_header(repo_data):
    """
    Function that adds category information extracted using header information
    Parameters
    ----------
    repo_data data to use the header analysis

    Returns
    -------
    Returns json with the information added.
    """
    print("Extracting information using headers")
    # this is a hack because if repo_data is "" this errors out
    if len(repo_data) == 0:
        return {}, []
    try:
        header_info, string_list = header_analysis.extract_categories_using_headers(repo_data)
        print("Information extracted. \n")
        return header_info, string_list
    except:
        print("Error while extracting headers: ", sys.exc_info()[0])
        return {}, [repo_data]


def extract_bibtex(readme_text) -> object:
    """
    Function takes readme text as input (cleaned from markdown notation) and runs a regex expression on top of it.
    Returns list of bibtex citations
    """
    regex = r'\@[a-zA-Z]+\{[.\n\S\s]+?[author|title][.\n\S\s]+?[author|title][.\n\S\s]+?\n\}'
    citations = re.findall(regex, readme_text)
    print("Extraction of bibtex citation from readme completed. \n")
    return citations


def extract_dois(readme_text) -> object:
    """
    Function that takes the text of a readme file and searches if there are any DOIs badges.
    Parameters
    ----------
    readme_text Text of the readme

    Returns
    -------
    DOIs/identifiers associated with this software component
    """
    # regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    # regex = r'\[\!\[DOI\]\(.+\)\]\(([^)]+)\)'
    regex = r'\[\!\[DOI\]([^\]]+)\]\(([^)]+)\)'
    dois = re.findall(regex, readme_text)
    print("Extraction of DOIS from readme completed.\n")
    return dois


def extract_binder_links(readme_text) -> object:
    """
    Function that does a regex to extract binder links used as reference in the readme.
    There could be multiple binder links for one reprository
    Parameters
    ----------
    readme_text

    Returns
    -------
    Links with binder notebooks/scripts that are ready to be executed.
    """
    regex = r'\[\!\[Binder\]([^\]]+)\]\(([^)]+)\)'
    binder_links = re.findall(regex, readme_text)
    print("Extraction of Binder links from readme completed.\n")
    # remove duplicates
    return list(dict.fromkeys(binder_links))


def extract_title(unfiltered_text):
    html_text = markdown.markdown(unfiltered_text)
    splitted = html_text.split("\n")
    index = 0
    limit = len(splitted)
    output = ""
    regex = r'<[^<>]+>'
    while index < limit:
        line = splitted[index]
        if line.startswith("<h"):
            if line.startswith("<h1>"):
                output = re.sub(regex, '', line)
            break
        index += 1
    return output


def extract_title_old(unfiltered_text):
    """
    Function to extract a title based on the first header in the readme file
    Parameters
    ----------
    unfiltered_text unfiltered text of the title

    Returns
    -------
    Full title of the repo (if found)
    """
    underline_header = re.findall('.+[\n]={3,}[\n]', unfiltered_text)
    # header declared with ====
    title = ""
    if len(underline_header) != 0:
        title = re.split('.+[=]+[\n]+', unfiltered_text)[0].strip()
    else:
        # The first occurrence is assumed to be the title.
        title = re.findall(r'# .+', unfiltered_text)[0]
        # Remove initial #
        if title is not None and len(title) > 0:
            title = title[1:].strip()
    # Remove other markup (links, etc.)
    if "[!" in title:
        title = re.split('\[\!', title)[0].strip()
    # title = re.sub(r'/\[\!([^\[\]]*)\]\((.*?)\)', '',title)
    return title


def extract_readthedocs(readme_text) -> object:
    """
    Function to extract readthedocs links from text
    Parameters
    ----------
    unfiltered_text text readme

    Returns
    -------
    Links to the readthedocs documentation
    """
    regex = r'http[s]?://[\w]+.readthedocs.io/'
    readthedocs_links = re.findall(regex, readme_text)
    print("Extraction of readthedocs links from readme completed.\n")
    # remove duplicates (links like [readthedocs](readthedocs) are found twice
    return list(dict.fromkeys(readthedocs_links))


def extract_support_channels(readme_text):
    """
    Function to extract Gitter Chat, Reddit and Discord links from text
    Parameters
    ----------
    readme_text text readme

    Returns
    -------
    Link to the Gitter Chat
    """
    results = []

    index_gitter_chat = readme_text.find("[![Gitter chat]")
    if index_gitter_chat > 0:
        init = readme_text.find(")](", index_gitter_chat)
        end = readme_text.find(")", init + 3)
        gitter_chat = readme_text[init + 3:end]
        results.append(gitter_chat)

    init = readme_text.find("(https://www.reddit.com/r/")
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    init = readme_text.find("(https://discord.com/invite/")
    if init > 0:
        end = readme_text.find(")", init)
        repo_status = readme_text[init + 1:end]
        results.append(repo_status)

    return results


def extract_repo_status(unfiltered_text):
    repo_status = ""
    init = unfiltered_text.find("[![Project Status:")
    if init > 0:
        end = unfiltered_text.find("](", init)
        repo_status = unfiltered_text[init + 3:end]
        repo_status = repo_status.replace("Project Status: ", "")
    return repo_status


def extract_arxiv_links(unfiltered_text):
    result_links = [m.start() for m in re.finditer('https://arxiv.org/', unfiltered_text)]
    result_refs = [m.start() for m in re.finditer('arXiv:', unfiltered_text)]
    results = []
    for position in result_links:
        end = unfiltered_text.find(')', position)
        link = unfiltered_text[position:end]
        results.append(link)
    for position in result_refs:
        end = unfiltered_text.find('}', position)
        link = unfiltered_text[position:end]
        results.append(link.replace('arXiv:', 'https://arxiv.org/abs/'))

    return results


# TO DO: join with image detection in a single method
def extract_logo(unfiltered_text, repo_url):
    logo = ""
    index_logo = unfiltered_text.lower().find("![logo]")
    if index_logo >= 0:
        init = unfiltered_text.find("(", index_logo)
        end = unfiltered_text.find(")", init)
        logo = unfiltered_text[init + 1:end]
    else:
        # This is problematic if alt label is used
        # TO DO
        result = [_.start() for _ in re.finditer("<img src=", unfiltered_text)]
        if len(result) > 0:
            for index_img in result:
                init = unfiltered_text.find("\"", index_img)
                end = unfiltered_text.find("\"", init + 1)
                img = unfiltered_text[init + 1:end]
                if img.find("logo") > 0:
                    logo = img

    if logo != "" and not logo.startswith("http") and repo_url is not None:
        if repo_url.find("github.com") > 0:
            if repo_url.find("/tree/") > 0:
                repo_url = repo_url.replace("/tree/", "/")
            else:
                repo_url = repo_url + "/master/"
            repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
            if not repo_url.endswith("/"):
                repo_url = repo_url + "/"
            logo = repo_url + logo
        else:
            if not repo_url.endswith("/"):
                repo_url = repo_url + "/"
            logo = repo_url + logo
    print(logo)
    return logo


# TO DO: join with logo detection
def extract_images(unfiltered_text, repo_url):
    logo = ""
    images = []
    html_text = markdown.markdown(unfiltered_text)
    # print(html_text)
    result = [_.start() for _ in re.finditer("<img ", html_text)]
    if len(result) > 0:
        for index_img in result:
            init = html_text.find("src=\"", index_img)
            end = html_text.find("\"", init + 5)
            img = html_text[init + 5:end]
            if img.find("logo") < 0:
                if not img.startswith("http") and repo_url is not None:
                    if repo_url.find("/tree/") > 0:
                        repo_url = repo_url.replace("/tree/", "/")
                    else:
                        repo_url = repo_url + "/master/"
                    repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
                    if not repo_url.endswith("/"):
                        repo_url = repo_url + "/"
                    img = repo_url + img
                images.append(img)
            else:
                if not img.startswith("http") and repo_url is not None:
                    if repo_url.find("/tree/") > 0:
                        repo_url = repo_url.replace("/tree/", "/")
                    else:
                        repo_url = repo_url + "/master/"
                    repo_url = repo_url.replace("github.com", "raw.githubusercontent.com")
                    if not repo_url.endswith("/"):
                        repo_url = repo_url + "/"
                    img = repo_url + img
                logo = img

    return logo, images


def extract_support(unfiltered_text):
    results = []
    init = unfiltered_text.find("(https://www.reddit.com/r/")
    if init > 0:
        end = unfiltered_text.find(")", init)
        repo_status = unfiltered_text[init + 1:end]
        results.append(repo_status)

    init = unfiltered_text.find("(https://discord.com/invite/")
    if init > 0:
        end = unfiltered_text.find(")", init)
        repo_status = unfiltered_text[init + 1:end]
        results.append(repo_status)

    return results


def merge(header_predictions, predictions, citations, citation_file_text, dois, binder_links, long_title,
          readthedocs_links, repo_status, arxiv_links, logo, images, support_channels):
    """
    Function that takes the predictions using header information, classifier and bibtex/doi parser
    Parameters
    ----------
    header_predictions extraction of common headers and their contents
    predictions predictions from classifiers (description, installation instructions, invocation, citation)
    citations (bibtex citations)
    dois identifiers found in readme (Zenodo DOIs)

    Returns
    -------
    Combined predictions and results of the extraction process
    """
    print("Merge prediction using header information, classifier and bibtex and doi parsers")
    if long_title:
        predictions['longTitle'] = {'excerpt': long_title, 'confidence': [1.0],
                                    'technique': 'Regular expression'}
    for i in range(len(citations)):
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        predictions['citation'].insert(0, {'excerpt': citations[i], 'confidence': [1.0],
                                           'technique': 'Regular expression'})
    if len(citation_file_text) != 0:
        if 'citation' not in predictions.keys():
            predictions['citation'] = []
        predictions['citation'].insert(0, {'excerpt': citation_file_text, 'confidence': [1.0],
                                           'technique': 'File Exploration'})
    if len(dois) != 0:
        predictions['identifier'] = []
        for identifier in dois:
            # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
            predictions['identifier'].insert(0, {'excerpt': identifier[1], 'confidence': [1.0],
                                                 'technique': 'Regular expression'})
    if len(binder_links) != 0:
        predictions['executableExample'] = []
        for notebook in binder_links:
            # The identifier is in position 1. Position 0 is the badge id, which we don't want to export
            predictions['executableExample'].insert(0, {'excerpt': notebook[1], 'confidence': [1.0],
                                                        'technique': 'Regular expression'})

    if len(repo_status) != 0:
        predictions['repoStatus'] = {
            'excerpt': "https://www.repostatus.org/#" + repo_status[0:repo_status.find(" ")].lower(),
            'description': repo_status,
            'technique': 'Regular expression'}

    if len(arxiv_links) != 0:
        predictions['arxivLinks'] = {'excerpt': arxiv_links, 'confidence': [1.0],
                                     'technique': 'Regular expression'}

    if len(logo) != 0:
        predictions['logo'] = {'excerpt': logo, 'confidence': [1.0],
                               'technique': 'Regular expression'}

    if len(images) != 0:
        predictions['image'] = []
        for image in images:
            predictions['image'].insert(0, {'excerpt': image, 'confidence': [1.0],
                                            'technique': 'Regular expression'})

    if len(support_channels) != 0:
        predictions['supportChannels'] = {'excerpt': support_channels, 'confidence': [1.0],
                                          'technique': 'Regular expression'}

    for i in range(len(readthedocs_links)):
        if 'documentation' not in predictions.keys():
            predictions['documentation'] = []
        predictions['documentation'].insert(0, {'excerpt': readthedocs_links[i], 'confidence': [1.0],
                                                'technique': 'Regular expression'})
    for headers in header_predictions:
        if headers not in predictions.keys():
            predictions[headers] = header_predictions[headers]
        else:
            for h in header_predictions[headers]:
                predictions[headers].insert(0, h)
    print("Merging successful. \n")
    return predictions


def format_output(git_data, repo_data, gitlab_url=False):
    """
    Function takes metadata, readme text predictions, bibtex citations and path to the output file
    Performs some combinations
    Parameters
    ----------
    git_data GitHub obtained data
    repo_data Data extracted from the code repo by SOMEF

    Returns
    -------
    json representation of the categories found in file
    """
    text_technigue = 'GitHub API'
    if gitlab_url:
        text_technigue = 'GitLab API'
    print("formatting output")
    file_exploration = ['hasExecutableNotebook', 'hasBuildFile', 'hasDocumentation', 'codeOfConduct',
                        'contributingGuidelines', 'licenseFile', 'licenseText', 'acknowledgments', 'contributors',
                        'hasScriptFile']
    for i in git_data.keys():
        # print(i)
        # print(git_data[i])
        if i == 'description':
            if 'description' not in repo_data.keys():
                repo_data['description'] = []
            if git_data[i] != "":
                repo_data['description'].append(
                    {'excerpt': git_data[i], 'confidence': [1.0], 'technique': text_technigue})
        else:
            if i in file_exploration:
                repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': 'File Exploration'}
            elif git_data[i] != "" and git_data[i] != []:
                repo_data[i] = {'excerpt': git_data[i], 'confidence': [1.0], 'technique': text_technigue}
    # remove empty categories from json
    return remove_empty_elements(repo_data)


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


# saves the final json Object in the file
def save_json_output(repo_data, outfile, missing, pretty=False):
    print("Saving json data to", outfile)
    if missing:
        missing = create_missing_fields(repo_data)
        repo_data["missingCategories"] = missing["missingCategories"]
    with open(outfile, 'w') as output:
        if pretty:
            json.dump(repo_data, output, sort_keys=True, indent=2)
        else:
            json.dump(repo_data, output)

    ## Function takes metadata, readme text predictions, bibtex citations and path to the output file


## Performs some combinations and saves the final json Object in the file
def save_json(git_data, repo_data, outfile):
    repo_data = format_output(git_data, repo_data)
    save_json_output(repo_data, outfile, None)


def save_codemeta_output(repo_data, outfile, pretty=False):
    def data_path(path):
        return DataGraph.resolve_path(repo_data, path)

    def format_date(date_string):
        date_object = date_parser.parse(date_string)
        return date_object.strftime("%Y-%m-%d")

    latest_release = None
    releases = data_path(["releases", "excerpt"])

    if releases is not None and len(releases) > 0:
        latest_release = releases[0]
        latest_pub_date = date_parser.parse(latest_release["datePublished"])
        for index in range(1, len(releases)):
            release = releases[index]
            pub_date = date_parser.parse(release["datePublished"])

            if pub_date > latest_pub_date:
                latest_release = release
                latest_pub_date = pub_date

    def release_path(path):
        return DataGraph.resolve_path(latest_release, path)

    code_repository = None
    if "codeRepository" in repo_data:
        code_repository = data_path(["codeRepository", "excerpt"])

    author_name = data_path(["owner", "excerpt"])

    # do the descriptions

    def average_confidence(x):
        confs = x["confidence"]

        if len(confs) > 0:
            try:
                return max(sum(confs) / len(confs))
            except:
                return 0
        else:
            return 0

    descriptions = data_path(["description"])
    descriptions_text = []
    if descriptions is not None:
        descriptions.sort(key=lambda x: (average_confidence(x) + (1 if x["technique"] == "GitHub API" else 0)),
                          reverse=True)
        descriptions_text = [x["excerpt"] for x in descriptions]

    published_date = ""
    try:
        published_date = format_date(release_path(["datePublished"]))
    except:
        print("Published date is not available")

    codemeta_output = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode"
    }
    if "license" in repo_data:
        codemeta_output["license"] = data_path(["license", "excerpt"])
    if code_repository is not None:
        codemeta_output["codeRepository"] = "git+" + code_repository + ".git"
        codemeta_output["issueTracker"] = code_repository + "/issues"
    if "dateCreated" in repo_data:
        codemeta_output["dateCreated"] = format_date(data_path(["dateCreated", "excerpt"]))
    if "dateModified" in repo_data:
        codemeta_output["dateModified"] = format_date(data_path(["dateModified", "excerpt"]))
    if "downloadUrl" in repo_data:
        codemeta_output["downloadUrl"] = data_path(["downloadUrl", "excerpt"])
    if "name" in repo_data:
        codemeta_output["name"] = data_path(["name", "excerpt"])
    if "releases" in repo_data:
        codemeta_output["releaseNotes"] = release_path(["body"])
        codemeta_output["version"] = release_path(["tag_name"])
    if "topics" in repo_data:
        codemeta_output["keywords"] = data_path(["topics", "excerpt"])
    if "languages" in repo_data:
        codemeta_output["programmingLanguage"] = data_path(["languages", "excerpt"])
    if "requirement" in repo_data:
        codemeta_output["softwareRequirements"] = data_path(["requirement", "excerpt"])
    if "installation" in repo_data:
        codemeta_output["buildInstructions"] = data_path(["installation", "excerpt"])
    if "owner" in repo_data:
        codemeta_output["author"] = [
            {
                "@type": "Person",
                "@id": "https://github.com/" + author_name
            }
        ]
    if "acknowledgement" in repo_data:
        codemeta_output["acknowledgement"] = data_path(["acknowledgement", "excerpt"])
    if "support" in repo_data:
        codemeta_output["support"] = data_path(["support", "excerpt"])
    if "citation" in repo_data:
        codemeta_output["citation"] = data_path(["citation", "excerpt"])
    if "citationFile" in repo_data:
        codemeta_output["citationFile"] = data_path(["citationFile", "excerpt"])
    if "codeOfConduct" in repo_data:
        codemeta_output["codeOfConduct"] = data_path(["codeOfConduct", "excerpt"])
    if "forks_count" in repo_data:
        codemeta_output["forks_count"] = data_path(["forks_count", "excerpt"])
    if "forks_url" in repo_data:
        codemeta_output["forks_url"] = data_path(["forks_url", "excerpt"])
    if "fullName" in repo_data:
        codemeta_output["fullName"] = data_path(["fullName", "excerpt"])
    if "hasBuildFile" in repo_data:
        codemeta_output["hasBuildFile"] = data_path(["hasBuildFile", "excerpt"])
    if "hasDocumentation" in repo_data:
        codemeta_output["hasDocumentation"] = data_path(["hasDocumentation", "excerpt"])
    if "hasExecutableNotebook" in repo_data:
        codemeta_output["hasExecutableNotebook"] = data_path(["hasExecutableNotebook", "excerpt"])
    if "identifier" in repo_data:
        codemeta_output["identifier"] = data_path(["identifier", "excerpt"])
    if "invocation" in repo_data:
        codemeta_output["invocation"] = data_path(["invocation", "excerpt"])
    if "issueTracker" in repo_data:
        codemeta_output["issueTracker"] = data_path(["issueTracker", "excerpt"])
    if "name" in repo_data:
        codemeta_output["name"] = data_path(["name", "excerpt"])
    if "ownerType" in repo_data:
        codemeta_output["ownerType"] = data_path(["ownerType", "excerpt"])
    if "readme_url" in repo_data:
        codemeta_output["readme_url"] = data_path(["readme_url", "excerpt"])
    if "stargazers_count" in repo_data:
        codemeta_output["stargazers_count"] = data_path(["stargazers_count", "excerpt"])
    if "arxivLinks" in repo_data:
        codemeta_output["arxivLinks"] = data_path(["arxivLinks", "excerpt"])
    if "codeOfConduct" in repo_data:
        codemeta_output["codeOfConduct"] = data_path(["codeOfConduct", "excerpt"])
    if "contributingGuidelines" in repo_data:
        codemeta_output["contributingGuidelines"] = data_path(["contributingGuidelines", "excerpt"])
    if "contributingGuidelinesFile" in repo_data:
        codemeta_output["contributingGuidelinesFile"] = data_path(["contributingGuidelinesFile", "excerpt"])
    if "licenseFile" in repo_data:
        codemeta_output["licenseFile"] = data_path(["licenseFile", "excerpt"])
    if "licenseText" in repo_data:
        codemeta_output["licenseText"] = data_path(["licenseText", "excerpt"])
    if "acknowledgments" in repo_data:
        codemeta_output["acknowledgments"] = data_path(["acknowledgments", "excerpt"])
    if "acknowledgmentsFile" in repo_data:
        codemeta_output["acknowledgmentsFile"] = data_path(["acknowledgmentsFile", "excerpt"])
    if "contributors" in repo_data:
        codemeta_output["contributors"] = data_path(["contributors", "excerpt"])
    if "contributorsFile" in repo_data:
        codemeta_output["contributorsFile"] = data_path(["contributorsFile", "excerpt"])
    if "hasScriptFile" in repo_data:
        codemeta_output["hasScriptFile"] = data_path(["hasScriptFile", "excerpt"])
    if "executableExample" in repo_data:
        codemeta_output["executableExample"] = data_path(["executableExample", "excerpt"])
    if descriptions_text:
        codemeta_output["description"] = descriptions_text
    if published_date != "":
        codemeta_output["datePublished"] = published_date
    pruned_output = {}

    for key, value in codemeta_output.items():
        if not (value is None or ((isinstance(value, list) or isinstance(value, tuple)) and len(value) == 0)):
            pruned_output[key] = value

    # now, prune out the variables that are None

    save_json_output(pruned_output, outfile, None, pretty=pretty)


def create_missing_fields(repo_data):
    """Function to create a small report with the categories SOMEF was not able to find"""
    categs = ["installation", "citation", "acknowledgement", "run", "download", "requirement", "contact", "description",
              "contributor", "documentation", "license", "usage", "faq", "support", "identifier",
              "hasExecutableNotebook", "hasBuildFile", "hasDocumentation", "executableExample"]
    missing = []
    out = {}
    for c in categs:
        if c not in repo_data:
            missing.append(c)
    out["missingCategories"] = missing
    return out


def create_missing_fields_report(repo_data, out_path):
    """Function to create a small report with the categories SOMEF was not able to find"""
    categs = ["installation", "citation", "acknowledgement", "run", "download", "requirement", "contact", "description",
              "contributor", "documentation", "license", "usage", "faq", "support", "identifier",
              "hasExecutableNotebook", "hasBuildFile", "hasDocumentation", "executableExample"]
    missing = []
    out = {}
    for c in categs:
        if c not in repo_data:
            missing.append(c)
    out["missing"] = missing
    export_path = ""
    if "json" in out_path:
        export_path = out_path.replace(".json", "_missing.json")
    if "ttl" in out_path:
        export_path = out_path.replace(".ttl", "_missing.json")
    else:
        export_path = out_path + "_missing.json"
    save_json_output(out, export_path, False)


def cli_get_data(threshold, ignore_classifiers, repo_url=None, doc_src=None, local_repo=None):
    credentials_file = Path(
        os.getenv("SOMEF_CONFIGURATION_FILE", '~/.somef/config.json')
    ).expanduser()
    if credentials_file.exists():
        with credentials_file.open("r") as fh:
            file_paths = json.load(fh)
    else:
        sys.exit("Error: Please provide a config.json file.")
    header = {}
    if 'Authorization' in file_paths.keys():
        header['Authorization'] = file_paths['Authorization']
    header['accept'] = 'application/vnd.github.v3+json'
    if repo_url is not None:
        assert (doc_src is None)
        try:
            text, github_data = load_repository_metadata(repo_url, header)
            if text == "":
                print("Warning: README document does not exist in the repository")
        except GithubUrlError:
            return None
    elif local_repo is not None:
        assert (local_repo is not None)
        try:
            text, github_data = load_local_repository_metadata(local_repo)
            if text == "":
                print("Warning: README document does not exist in the local repository")
        except GithubUrlError:
            return None
    else:
        assert (doc_src is not None)
        if not path.exists(doc_src):
            sys.exit("Error: Document does not exist at given path")
        with open(doc_src, 'r') as doc_fh:
            text = doc_fh.read()
        github_data = {}

    unfiltered_text = text
    header_predictions, string_list = extract_categories_using_header(unfiltered_text)
    text = unmark(text)
    excerpts = create_excerpts(string_list)
    if ignore_classifiers or unfiltered_text == '':
        predictions = {}
    else:
        excerpts_headers = parser_somef.extract_text_excerpts_header(unfiltered_text)
        header_parents = parser_somef.extract_headers_parents(unfiltered_text)
        score_dict = run_classifiers(excerpts, file_paths)
        predictions = classify(score_dict, threshold, excerpts_headers, header_parents)
    if text != '':
        citations = extract_bibtex(text)
        citation_file_text = ""
        if 'citation' in github_data.keys():
            citation_file_text = github_data['citation']
            del github_data['citation']
        dois = extract_dois(unfiltered_text)
        binder_links = extract_binder_links(unfiltered_text)
        title = extract_title(unfiltered_text)
        readthedocs_links = extract_readthedocs(unfiltered_text)
        repo_status = extract_repo_status(unfiltered_text)
        arxiv_links = extract_arxiv_links(unfiltered_text)
        #logo = extract_logo(unfiltered_text, repo_url)
        logo, images = extract_images(unfiltered_text, repo_url)
        support_channels = extract_support_channels(unfiltered_text)
    else:
        citations = []
        citation_file_text = ""
        dois = []
        binder_links = []
        title = ""
        readthedocs_links = []
        repo_status = ""
        arxiv_links = []
        logo = ""
        images = []
        support_channels = []

    predictions = merge(header_predictions, predictions, citations, citation_file_text, dois, binder_links, title,
                        readthedocs_links, repo_status, arxiv_links, logo, images, support_channels)
    gitlab_url = False
    if repo_url is not None:
        if repo_url.rfind("gitlab.com") > 0:
            gitlab_url = True
    return format_output(github_data, predictions, gitlab_url)


# Function runs all the required components of the cli on a given document file
def run_cli_document(doc_src, threshold, output):
    return run_cli(threshold=threshold, output=output, doc_src=doc_src)


# Function runs all the required components of the cli for a repository
def run_cli(*,
            threshold=0.8,
            ignore_classifiers=False,
            repo_url=None,
            doc_src=None,
            local_repo=None,
            in_file=None,
            output=None,
            graph_out=None,
            graph_format="turtle",
            codemeta_out=None,
            pretty=False,
            missing=False
            ):
    # check if it is a valid url
    if repo_url:
        if not validators.url(repo_url):
            print("Not a valid repository url. Please check the url provided")
            return None
    multiple_repos = in_file is not None
    if multiple_repos:
        with open(in_file, "r") as in_handle:
            # get the line (with the final newline omitted) if the line is not empty
            repo_list = [line[:-1] for line in in_handle if len(line) > 1]

        # convert to a set to ensure uniqueness (we don't want to get the same data multiple times)
        repo_set = set(repo_list)
        # check if the urls in repo_set if are valids
        remove_urls = []
        for repo_elem in repo_set:
            if not validators.url(repo_elem):
                print("Not a valid repository url. Please check the url provided: " + repo_elem)
                # repo_set.remove(repo_url)
                remove_urls.append(repo_elem)
        # remove non valid urls in repo_set
        for remove_url in remove_urls:
            repo_set.remove(remove_url)
        if len(repo_set) > 0:
            repo_data = [cli_get_data(threshold, ignore_classifiers, repo_url=repo_url) for repo_url in repo_set]
        else:
            return None

    else:
        if repo_url:
            repo_data = cli_get_data(threshold, ignore_classifiers, repo_url=repo_url)
        elif local_repo:
            repo_data = cli_get_data(threshold, ignore_classifiers, local_repo=local_repo)
        else:
            repo_data = cli_get_data(threshold, ignore_classifiers, doc_src=doc_src)

    if output is not None:
        save_json_output(repo_data, output, missing, pretty=pretty)

    if graph_out is not None:
        print("Generating Knowledge Graph")
        data_graph = DataGraph()
        if multiple_repos:
            for repo in repo_data:
                data_graph.add_somef_data(repo)
        else:
            data_graph.add_somef_data(repo_data)

        print("Saving Knowledge Graph ttl data to", graph_out)
        with open(graph_out, "wb") as out_file:
            out_file.write(data_graph.g.serialize(format=graph_format, encoding="UTF-8"))

    if codemeta_out is not None:
        save_codemeta_output(repo_data, codemeta_out, pretty=pretty)

    if missing is True:
        # save in the same path as output
        # if output is not None:
        #    create_missing_fields_report(repo_data, output)
        # elif codemeta_out is not None:
        if codemeta_out is not None:
            create_missing_fields_report(repo_data, codemeta_out)
        elif graph_out is not None:
            create_missing_fields_report(repo_data, graph_out)
