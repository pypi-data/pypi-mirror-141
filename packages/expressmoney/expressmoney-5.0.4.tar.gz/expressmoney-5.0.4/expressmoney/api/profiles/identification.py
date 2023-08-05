__all__ = ()

from expressmoney.api import *
from expressmoney.viewflow import status

SERVICE_NAME = 'profiles'


class RussiaReadContract(Contract):
    EMPTY = status.EMPTY
    IN_PROCESS = status.IN_PROCESS
    SUCCESS = status.SUCCESS
    ERROR = status.ERROR
    FAILURE = status.FAILURE
    RETRY = status.RETRY

    AUTO_RESULT_CHOICES = (
        (IN_PROCESS, ' In process'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
        (FAILURE, 'Failure'),
    )

    MANUAL_RESULT_CHOICES = (
        (SUCCESS, 'Success'),
        (RETRY, 'Retry'),
        (FAILURE, 'Failure'),
    )
    pagination = PaginationContract()
    id = serializers.IntegerField(min_value=1)
    status = serializers.CharField(max_length=50)
    updated = serializers.DateField(auto_now=True)
    profile = serializers.IntegerField(min_value=1)
    attempts = serializers.IntegerField(min_value=0)
    auto_result = serializers.ChoiceField(choices=AUTO_RESULT_CHOICES)
    request_id = serializers.CharField(max_length=128, allow_blank=True)
    manual_result = serializers.ChoiceField(choices=MANUAL_RESULT_CHOICES)
    comment = serializers.CharField(max_length=1024, allow_blank=True)
    first_name = serializers.CharField(max_length=32)
    first_name_old = serializers.CharField(max_length=32, allow_blank=True)
    last_name = serializers.CharField(max_length=32)
    last_name_old = serializers.CharField(max_length=32, allow_blank=True)
    middle_name = serializers.CharField(max_length=32)
    middle_name_old = serializers.CharField(max_length=32, allow_blank=True)
    passport_serial = serializers.CharField(max_length=4)
    passport_serial_old = serializers.CharField(max_length=4, allow_blank=True)
    passport_number = serializers.CharField(max_length=6)
    passport_number_old = serializers.CharField(max_length=6, allow_blank=True)


profiles_identification_russia = ID(SERVICE_NAME, 'identification', 'russia')


class RussiaPoint(ListPointMixin, ContractPoint):
    _point_id = profiles_identification_russia
    _read_contract = RussiaReadContract
