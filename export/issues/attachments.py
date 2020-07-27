import os
from datetime import datetime, timezone, tzinfo, timedelta
from random import randint

current_year = datetime.now().year


def get_random_date_underscored(date_timezone: tzinfo = None):
    return datetime(year=randint(2005, current_year),
                    month=randint(1, 12),
                    day=randint(1, 28),
                    tzinfo=date_timezone)\
        .strftime('%Y_%m_%d')


def get_random_date_iso(date_timezone=None):

    return datetime(year=randint(2005, current_year),
                    month=randint(1, 12),
                    day=randint(1, 28),
                    tzinfo=date_timezone)\
        .isoformat()


def mkdir_if_not_exists(path):
    try:
        # create the directory if it doesn't already exist
        os.mkdir(path)
    except FileExistsError:
        # ignore the error, this means the path exists
        pass


def mock_dir(path, project_key='ABC', num_issues=10, num_attachments_per_issue=2,
             fileattachment_table_csv_export_file_name='fileattachment.csv', dates_hours_diff=0):

    if not project_key:
        raise ValueError('project_key cannot be empty')

    if 1 > num_issues > 10000:
        raise ValueError('num_issues cannot be less than 1 or more than 10 000')

    if 1 > num_attachments_per_issue > 100:
        raise ValueError('num_attachments_per_issue cannot be less than 1 or more than 100')

    if not fileattachment_table_csv_export_file_name:
        raise ValueError('fileattachment_table_csv_export cannot be empty')

    mkdir_if_not_exists(path)

    dates_timezone = timezone(timedelta(hours=dates_hours_diff))
    with open(f'{path}/{fileattachment_table_csv_export_file_name}', 'w') as f:
        # write the header for the csv
        f.write('id,issueid,mimetype,filename,created,filesize,author,zip,thumbnailable\n')

        issue_id = 100
        attachment_id = 1
        for issue_key in range(1, num_issues + 1):
            issue_path = f'{path}/{project_key}-{issue_key}'
            mkdir_if_not_exists(issue_path)

            for _ in range(num_attachments_per_issue):
                with open(f'{issue_path}/{attachment_id}', 'w') as _:
                    pass

                mime_type = 'image/png'
                file_name = f'Screenshot_{get_random_date_underscored(dates_timezone)}.png'
                created = get_random_date_iso(dates_timezone)
                file_size = randint(1000, 10000)
                f.write(f'{attachment_id},{issue_id},{mime_type},{file_name},{created},{file_size},unknown,,1\n')
                attachment_id += 1

            issue_id += 1
