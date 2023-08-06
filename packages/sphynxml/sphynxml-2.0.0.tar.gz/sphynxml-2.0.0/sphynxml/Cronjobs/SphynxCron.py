from typing import List, Optional, Union

import crontab
from crontab import CronTab


# TODO: This needs rework
# TODO: COMMENT SHOULD BE UNIQUE ?!
# CHECK BEFORE ADDING A JOB
# MAKE IT MANDATORY
class SphynxCron:
    def __init__(self, user: Optional[str] = True):
        self.cron = CronTab(user=user)
        return

    def set_cronjob(
        self,
        command: str,
        comment: Optional[str] = "",
        minute: Optional[Union[int, str]] = "*",
        hour: Optional[Union[int, str]] = "*",
        dom: Optional[Union[int, str]] = "*",
        month: Optional[Union[int, str]] = "*",
        dow: Optional[Union[int, str]] = "*",
    ):
        """
        Sets a Cronjob task based on specific syntax. The syntax is specified below:

        ┌───────────── minute (0 - 59)
        │ ┌───────────── hour (0 - 23)
        │ │ ┌───────────── day of month (1 - 31)
        │ │ │ ┌───────────── month (1 - 12)
        │ │ │ │ ┌───────────── day of week (0 - 6) (Sunday to Saturday;
        │ │ │ │ │                                       7 is also Sunday on some systems)
        │ │ │ │ │
        │ │ │ │ │
        * * * * *  command to execute

        Parameters:
            command (str): The command
            comment (Optional[str]): The job comment (default: "")
            minute (Optional[Union[int, str]]): The minute value (default: '*')
            hour (Optional[Union[int, str]]): The hour value (default: '*')
            dom (Optional[Union[int, str]]): The day of month value (default: '*')
            month (Optional[Union[int, str]]): The month value (default: '*')
            dow (Optional[Union[int, str]]): The day of week value (default: '*')

        Returns:
            A CronTab with a new job

        """

        try:
            job = self.cron.new(command=command, comment=comment)
            str_time = f"{minute} {hour} {dom} {month} {dow}"
            job.setall(str_time)
            job.enable()
            self.cron.write()
        except ValueError:
            print("print error here")

        return job

    def set_recursive_cronjob(
        self, field: str, value: int, command: str, comment: Optional[str] = None
    ):
        """
        Sets a recursive Cronjob task based on specific field.

        Parameters:
            field (str): The field to set for the recursive task
            value (int): The
            command (str): The command
            comment (Optional[str]): The job comment (default: None)

        Returns:
            A CronTab with a new active job

        """

        job = self.cron.new(command=command, comment=comment)

        try:
            if field == "minute":
                job.minute.every(value)
            elif field == "hour":
                job.hour.every(value)
            elif field == "day_of_month":
                job.dom.every(value)
            elif field == "month":
                job.month.every(value)
            elif field == "year":
                job.year.every(value)
            elif field == "day_of_week":
                job.dow.every(value)

            job.enable()
            self.cron.write()
        except ValueError:
            print(f"Invalid value in {field} field")

        return job

    def list_jobs(self) -> List:
        """
        Returns all the jobs in the crontab.

        Returns:
            A list of the existing cronjobs

        """
        jobs = []
        for job in self.cron:
            jobs.append(job)

        return jobs

    def enable_job(self, job):
        """
        Sets the status of a job as disabled, meaning that the job is no
        longer active.

        Parameters:
            job (crontab.CronItem): The Cronjob to activate

        """
        job.enable(True)
        self.cron.write()
        return

    def disable_job(self, job):
        """
        Sets the status of a job as disabled, meaning that the job is no
        longer active.

        Parameters:
            job (crontab.CronItem): The Cronjob to disable

        """
        job.enable(False)
        self.cron.write()
        return

    def remove_job(self, job):
        """
        Removes a specific job from the crontab.

        Parameters:
            job (crontab.CronItem): The Cronjob to remove

        """
        self.cron.remove(job)
        self.cron.write()
        return
