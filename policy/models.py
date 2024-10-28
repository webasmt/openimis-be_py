from django.db import models
import uuid

class Policy(models.Model):
    id = models.AutoField(db_column='PolicyID', primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    policy_number = models.CharField(db_column='PolicyNumber', max_length=50, unique=True)
    start_date = models.DateField(db_column='StartDate')
    expiry_date = models.DateField(db_column='ExpiryDate', blank=True, null=True)
    status = models.CharField(db_column='Status', max_length=10)  # Exemple de statut : "active", "expired"

    audit_user_id = models.IntegerField(db_column='AuditUserID', blank=True, null=True)

    class Meta:
        db_table = 'tblPolicies'

    def __str__(self):
        return f"Policy {self.policy_number}"


class PolicyRenewal(models.Model):
    id = models.AutoField(db_column='RenewalID', primary_key=True)
    policy = models.ForeignKey('Policy', models.DO_NOTHING, related_name='renewals', db_column='PolicyID')
    renewal_date = models.DateField(db_column='RenewalDate')
    audit_user_id = models.IntegerField(db_column='AuditUserID', blank=True, null=True)

    class Meta:
        db_table = 'tblPolicyRenewals'

    def __str__(self):
        return f"Renewal for Policy {self.policy.policy_number} on {self.renewal_date}"