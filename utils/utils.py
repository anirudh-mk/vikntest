# from django.db.models import F, Func, Value, Window, ExpressionWrapper, BooleanField, Case, When, IntegerField
# from django.db.models.functions import Cast
# from django.db.models.functions.window import Lead
#
# from utils.enum import SettingsFlag
#
#
# class VoucherNumberUtils:
#
#     def __init__(self, model, company_id, branch_id, voucher_number, prefix, separator, suffix_separator, suffix,pad_length=30):
#         self.voucher_number = voucher_number
#         self.model = model
#         self.company_id = company_id
#         self.branch_id = branch_id
#         self.pad_length  = pad_length
#         self.generated_voucher_number = None
#         self.prefix = prefix
#         self.suffix = suffix
#         self.separator = separator
#         self.suffix_separator = suffix_separator
#
#     def _check_voucher_number_gap(self):
#         queryset = self.model.objects.annotate(
#             numeric_suffix=Func(
#                 F('VoucherNo'),
#                 Value(r'\d+$'),
#                 function='substring'
#             ),
#         ).exclude(numeric_suffix=None).annotate(
#             lp_voucher_number=Func(
#                 F('numeric_suffix'),
#                 Value(self.pad_length),
#                 Value('0'),
#                 function='lpad'
#             )
#         ).annotate(
#             next_voucher=Window(
#                 expression=Lead('lp_voucher_number'),
#                 order_by=F('lp_voucher_number').asc()
#             )
#         ).annotate(
#             current_numeric=Cast('lp_voucher_number', output_field=IntegerField()),
#             next_numeric=Cast('next_voucher', output_field=IntegerField())
#         ).annotate(
#             has_gap=Case(
#                 When(
#                     next_voucher__isnull=False,
#                     then=ExpressionWrapper(
#                         F('current_numeric') + 1 != F('next_numeric'),
#                         output_field=BooleanField()
#                     )
#                 ),
#                 default=Value(False),
#                 output_field=BooleanField()
#             ),
#             expected_next=ExpressionWrapper(
#                 F('current_numeric') + 1,
#                 output_field=IntegerField()
#             )
#         ).filter(
#             has_gap=True,
#             CompanyID__id=self.company_id,
#             BranchID=self.branch_id,
#         ).order_by('lp_voucher_number')
#
#         return queryset.values('expected_next').first(), queryset
#
#     def _generate_last_voucher_number(self,queryset):
#         """Generate the last voucher number based on the queryset."""
#         new_invoice_number = 0
#
#         if queryset.exists():
#             last_invoice_number = queryset.values('current_numeric').last()
#             new_invoice_number = last_invoice_number['current_numeric'] + 1
#
#         invoice_no = self._remove_leading_zeros(new_invoice_number)
#
#         return self.construct_voucher_number(invoice_no)
#
#     def construct_voucher_number(self, invoice_no):
#         """Construct the voucher number with leading zeros."""
#         return  f"{self.prefix}{self.separator}{invoice_no}{self.suffix_separator}{self.suffix}"
#
#     @staticmethod
#     def _remove_leading_zeros(invoice_no):
#         """Remove leading zeros."""
#         return str(invoice_no)
#
#     def is_voucher_no_exist(self):
#         return self.model.objects.filter(
#             CompanyID__id=self.company_id,
#             BranchID=self.branch_id,
#             VoucherNo=self.voucher_number
#         ).exists()
#
#     def is_voucher_no_auto_generate(self):
#
#         """Check if voucher number is set to auto-generate based on settings."""
#
#         if not SettingsFlag.VoucherNoAutoGenerate.value:
#             self.branch_id = 1
#
#         settings_value = GeneralSettings.objects.filter(
#                 CompanyID__id=self.company_id,
#                 BranchID=self.branch_id,
#                 SettingsType= SettingsFlag.VoucherNoAutoGenerate.value
#         ).values('SettingsValue').first()
#         if settings_value.get('SettingsValue') in {True, "True", "true"}:
#             return True
#         return False
#
#     def generate_voucher_no(self):
#
#         """Generate voucher number based on settings."""
#
#         if self.is_voucher_no_auto_generate():
#             voucher_no_gap, queryset = self._check_voucher_number_gap()
#             if voucher_no_gap:
#                 missing_invoice_no = voucher_no_gap['expected_next']
#                 invoice_no = self._remove_leading_zeros(missing_invoice_no)
#                 self.generated_voucher_number = self.construct_voucher_number(invoice_no)
#             else:
#                 self.generated_voucher_number = self._generate_last_voucher_number(queryset)
#         elif self.is_voucher_no_exist():
#             raise ValueError("Voucher number already exists.")
#         else:
#             self.generated_voucher_number = self.voucher_number
#
#         return self.generated_voucher_number

from django.db.models import F, Func, Value, Window, ExpressionWrapper, BooleanField, Case, When, IntegerField
from django.db.models.functions import Cast
from django.db.models.functions.window import Lead

from utils.enum import SettingsFlag
# from your_app.models import GeneralSettings  # Replace with actual model import


class VoucherNumberUtils:
    """
    Utility class for generating and managing voucher numbers in a Django model.

    Handles:
    - Auto-generation of voucher numbers
    - Gap detection in existing sequence
    - Formatting using prefix, suffix, and separators
    """

    def __init__(self, model, company_id, branch_id, voucher_number, prefix, separator, suffix_separator, suffix, pad_length=30):
        """
        Initialize the VoucherNumberUtils.

        Args:
            model (Model): Django model class with a VoucherNo field.
            company_id (int): Company ID for filtering.
            branch_id (int): Branch ID for filtering.
            voucher_number (str): User-provided voucher number (optional if auto-generating).
            prefix (str): Prefix to be added to the voucher number.
            separator (str): Separator between prefix and number.
            suffix_separator (str): Separator between number and suffix.
            suffix (str): Suffix to be added at the end.
            pad_length (int): Length to pad the numeric portion of voucher number.
        """
        self.voucher_number = voucher_number
        self.model = model
        self.company_id = company_id
        self.branch_id = branch_id
        self.pad_length = pad_length
        self.generated_voucher_number = None
        self.prefix = prefix
        self.suffix = suffix
        self.separator = separator
        self.suffix_separator = suffix_separator

    def _check_voucher_number_gap(self):
        """
        Identify gaps in the numeric sequence of existing voucher numbers.

        Returns:
            tuple:
                - dict: First missing voucher number in the sequence as {'expected_next': value}
                - QuerySet: Annotated queryset with numeric suffixes, gap info, etc.
        """
        queryset = self.model.objects.annotate(
            numeric_suffix=Func(
                F('VoucherNo'),
                Value(r'\d+$'),
                function='substring'
            ),
        ).exclude(numeric_suffix=None).annotate(
            lp_voucher_number=Func(
                F('numeric_suffix'),
                Value(self.pad_length),
                Value('0'),
                function='lpad'
            )
        ).annotate(
            next_voucher=Window(
                expression=Lead('lp_voucher_number'),
                order_by=F('lp_voucher_number').asc()
            )
        ).annotate(
            current_numeric=Cast('lp_voucher_number', output_field=IntegerField()),
            next_numeric=Cast('next_voucher', output_field=IntegerField())
        ).annotate(
            has_gap=Case(
                When(
                    next_voucher__isnull=False,
                    then=ExpressionWrapper(
                        F('current_numeric') + 1 != F('next_numeric'),
                        output_field=BooleanField()
                    )
                ),
                default=Value(False),
                output_field=BooleanField()
            ),
            expected_next=ExpressionWrapper(
                F('current_numeric') + 1,
                output_field=IntegerField()
            )
        ).filter(
            has_gap=True,
            CompanyID__id=self.company_id,
            BranchID=self.branch_id,
        ).order_by('lp_voucher_number')

        return queryset.values('expected_next').first(), queryset

    def _generate_last_voucher_number(self, queryset):
        """
        Generate the next voucher number based on the last existing one.

        Args:
            queryset (QuerySet): The annotated queryset used for gap checking.

        Returns:
            str: Newly generated voucher number.
        """
        new_invoice_number = 0

        if queryset.exists():
            last_invoice_number = queryset.values('current_numeric').last()
            new_invoice_number = last_invoice_number['current_numeric'] + 1

        invoice_no = self._remove_leading_zeros(new_invoice_number)
        return self.construct_voucher_number(invoice_no)

    def construct_voucher_number(self, invoice_no):
        """
        Construct the final formatted voucher number.

        Args:
            invoice_no (str or int): The numeric part of the voucher number.

        Returns:
            str: Fully constructed voucher number.
        """
        return f"{self.prefix}{self.separator}{invoice_no}{self.suffix_separator}{self.suffix}"

    @staticmethod
    def _remove_leading_zeros(invoice_no):
        """
        Convert invoice number to string (removing unintended leading zeros).

        Args:
            invoice_no (int or str): Invoice number.

        Returns:
            str: Clean string without unnecessary padding.
        """
        return str(invoice_no)

    def is_voucher_no_exist(self):
        """
        Check if the provided voucher number already exists.

        Returns:
            bool: True if it exists, False otherwise.
        """
        return self.model.objects.filter(
            CompanyID__id=self.company_id,
            BranchID=self.branch_id,
            VoucherNo=self.voucher_number
        ).exists()

    def is_voucher_no_auto_generate(self):
        """
        Determine whether voucher numbers should be auto-generated.

        Returns:
            bool: True if auto-generation is enabled in settings, False otherwise.
        """
        if not SettingsFlag.VoucherNoAutoGenerate.value:
            self.branch_id = 1

        settings_value = GeneralSettings.objects.filter(
            CompanyID__id=self.company_id,
            BranchID=self.branch_id,
            SettingsType=SettingsFlag.VoucherNoAutoGenerate.value
        ).values('SettingsValue').first()

        if settings_value.get('SettingsValue') in {True, "True", "true"}:
            return True
        return False

    def generate_voucher_no(self):
        """
        Generate the voucher number based on settings and existing data.

        Logic:
        - If auto-generation is enabled:
            - Fill any gap in existing sequence.
            - Else, generate next from the last number.
        - If manual and duplicate exists, raise error.

        Returns:
            str: The newly generated or validated voucher number.
        """
        if self.is_voucher_no_auto_generate():
            voucher_no_gap, queryset = self._check_voucher_number_gap()
            if voucher_no_gap:
                missing_invoice_no = voucher_no_gap['expected_next']
                invoice_no = self._remove_leading_zeros(missing_invoice_no)
                self.generated_voucher_number = self.construct_voucher_number(invoice_no)
            else:
                self.generated_voucher_number = self._generate_last_voucher_number(queryset)
        elif self.is_voucher_no_exist():
            raise ValueError("Voucher number already exists.")
        else:
            self.generated_voucher_number = self.voucher_number

        return self.generated_voucher_number
