import xml.dom.minidom
import requests

class Task:
    Status = "Unknown"
    Id = None
    DownloadUrl = None

    def is_active(self):
        if self.Status == "InProgress" or self.Status == "Queued":
            return True
        else:
            return False


def decode_response(xml_response):
    """ Decode xml response of the server. Return Task object """
    dom = xml.dom.minidom.parseString(xml_response)
    task_node = dom.getElementsByTagName("task")[0]
    task = Task()
    task.Id = task_node.getAttribute("id")
    task.Status = task_node.getAttribute("status")
    if task.Status == "Completed":
        task.DownloadUrl = task_node.getAttribute("resultUrl")
    return task


def get_task_status(task, applicationID, password):
    if task.Id.find('00000000-0') != -1:
        # GUID_NULL is being passed. This may be caused by a logical error in the calling code
        print("Null task id passed")
        return None

    url_params = {"taskId": task.Id}
    status_url = "http://cloud-eu.ocrsdk.com/getTaskStatus"

    response = requests.get(status_url, params=url_params,
                            auth=(applicationID, password), proxies={})
    task = decode_response(response.text)
    return task


def download_result(task):
    get_result_url = task.DownloadUrl
    if get_result_url is None:
        print("No download URL found")
        return

    file_response = requests.get(get_result_url, stream=True, proxies={})
    return file_response