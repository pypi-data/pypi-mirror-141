from os import environ
from requests import post


class Status:
    @staticmethod
    def __get_workitems() -> dict:
        """
        Get workitems data from robocorp cloud

        :param: None
        :return: dict
        """
        try:
            from RPA.Robocorp.WorkItems import WorkItems

            library = WorkItems()
            library.get_input_work_item()
            variables = library.get_work_item_variables()
            variables = variables["variables"]
        except ModuleNotFoundError:
            from RPA.Robocloud.Items import Items

            library = Items()
            library.load_work_item_from_environment()
            variables: dict = library.get_work_item_variables()

        return variables

    @staticmethod
    def change_status(status: str):
        """
        Change the status of the bot on TA

        :param status: The status on which needs to be changed. Can be 'warning'
        :return: None
        """
        items: dict = Status.__get_workitems()

        post(
            items["changeStatusUrl"],
            headers={"Authorization": f"Bearer {items['accessToken']}"},
            json={"runId": environ["RC_PROCESS_RUN_ID"], "newStatus": status},
        )

    @staticmethod
    def change_status_to_warning():
        """
        Change the status of the bot on TA to warning

        :param: None
        :return: None
        """
        Status.change_status("warning")
