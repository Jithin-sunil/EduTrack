from Administrator.models import tbl_auditlog

def log_action(usertype, userid, module, action):
    """
    Creates an entry in tbl_auditlog to capture who did what and when.
    """
    tbl_auditlog.objects.create(
        auditlog_usertype=usertype,
        auditlog_userid=userid,
        auditlog_module=module,
        auditlog_action=action
    )
