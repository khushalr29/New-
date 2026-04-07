from django.db import models
from ..core.employee import Employee
from .contract_type import ContractType

from ..core.base import TenantModel

class EmployeeContract(TenantModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employee_contract')
    contract_type = models.ForeignKey(ContractType, on_delete=models.CASCADE, related_name='employee_contract_type')
    start_date = models.DateField()
    end_date = models.DateField()
    basic_salary= models.PositiveIntegerField()
    terms_condition = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.full_name} - {self.contract_type.contract_type_name}"

