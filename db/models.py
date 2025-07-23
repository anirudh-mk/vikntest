from django.db import models
from django.utils.timezone import now
import uuid
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    # CompanyID = models.ForeignKey("brands.CompanySettings",on_delete=models.CASCADE,blank=True,null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CountryCode = models.CharField(max_length=128, blank=True, null=True)
    Country_Name = models.CharField(max_length=128, blank=True, null=True)
    Currency_Name = models.CharField(max_length=128, blank=True, null=True)
    Change = models.CharField(max_length=128, blank=True, null=True)
    Symbol = models.CharField(max_length=128, blank=True, null=True)
    FractionalUnits = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    CurrencySymbolUnicode = models.CharField(max_length=128, blank=True, null=True)
    ISD_Code = models.CharField(max_length=128, blank=True, null=True)
    # Flag = models.ImageField(upload_to="country-flags/", blank=True, null=True)
    Tax_Type = models.CharField(max_length=128, blank=True, null=True)
    IdentificationCode = models.CharField(max_length=2, blank=True, null=True)# https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#User-assigned_code_elements

    class Meta:
        db_table = "country_country"
        verbose_name = _("country")
        verbose_name_plural = _("countries")
        ordering = ("Country_Name",)

    def __unicode__(self):
        return str(self.Country_Name)
        # return smart_text(self.Country_Name)
    def __str__(self):
        return str(self.Country_Name)



class State(models.Model):
    Country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, blank=True, null=True, db_index=True, related_name='state_country'
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=128, blank=True, null=True)
    State_Type = models.CharField(max_length=128, blank=True, null=True)
    State_Code = models.CharField(max_length=128, blank=True, null=True)


class BusinessType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = "admin_business_type"
        verbose_name = _("business")
        verbose_name_plural = _("business")
        ordering = ("Name",)

    def __str__(self):
        return str(self.Name)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CreatedUserID = models.BigIntegerField(blank=True, null=True)
    UpdatedUserID = models.BigIntegerField(blank=True, null=True)
    CreatedDate = models.DateTimeField(db_index=True, auto_now_add=True)
    UpdatedDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class CompanySettings(BaseModel):
    Action = models.CharField(max_length=128, blank=True, null=True, default="A")
    CompanyName = models.CharField(max_length=128)
    CompanyNameSec = models.CharField(max_length=128, blank=True, null=True)
    # CompanyLogo = models.ImageField(upload_to="company-logo/", blank=True, null=True)
    District = models.CharField(max_length=128, blank=True, null=True)
    DistrictSec = models.CharField(max_length=128, blank=True, null=True)
    State = models.ForeignKey(
        "State", on_delete=models.PROTECT, blank=True, null=True
    )
    Country = models.ForeignKey(
        "Country", on_delete=models.PROTECT, blank=True, null=True, db_index=True
    )
    PostalCode = models.CharField(max_length=128, blank=True, null=True)
    PostalCodeSec = models.CharField(max_length=128, blank=True, null=True)
    Phone = models.CharField(max_length=150, blank=True, null=True)
    Mobile = models.CharField(max_length=150, blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Website = models.CharField(max_length=128, blank=True, null=True)
    business_type = models.ForeignKey(
        "BusinessType", on_delete=models.PROTECT, blank=True, null=True, db_index=True
    )
    owner = models.ForeignKey(
        "auth.User", related_name="user%(class)s_objects", on_delete=models.CASCADE
    )
    ExpiryDate = models.DateField(blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    LastUsedDate = models.DateTimeField(null=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    DeletedDate = models.DateTimeField(blank=True, null=True)
    CreatedUserID = models.BigIntegerField(blank=True, null=True)
    UpdatedUserID = models.BigIntegerField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    RegistrationType = models.CharField(max_length=128, blank=True, null=True)
    IsBranch = models.BooleanField(default=False)
    db = models.IntegerField(default=0)
    FaeraDevices = models.IntegerField(default=0)
    NoOfUsers = models.PositiveIntegerField(blank=True, null=True, default=1)

    NoOfBrances = models.PositiveIntegerField(blank=True, null=True, default=0) # not needed
    Address1 = models.CharField(max_length=150, blank=True, null=True) # Changed to Branch --->buildingNO
    Address1Sec = models.CharField(max_length=150, blank=True, null=True) # Changed to Branch
    Address2 = models.CharField(max_length=150, blank=True, null=True) #---> street
    Address2Sec = models.CharField(max_length=150, blank=True, null=True) # Changed to Branch
    Address3 = models.CharField(max_length=150, blank=True, null=True) # Changed to Branch #---> street
    City = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    CitySec = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    # Currency = models.BigIntegerField(blank=True,null=True)
    # FractionalUnit = models.BigIntegerField(blank=True,null=True)
    VATNumber = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    GSTNumber = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    LUTNumber = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch

    Tax1 = models.CharField(max_length=128, blank=True, null=True)# not need this column Nashid
    Tax2 = models.CharField(max_length=128, blank=True, null=True)# not need this column Nashid
    Tax3 = models.CharField(max_length=128, blank=True, null=True)# not need this column Nashid
    is_vat = models.BooleanField(default=False) # Changed to Branch
    is_gst = models.BooleanField(default=False) # Changed to Branch
    CRNumber = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    CINNumber = models.CharField(max_length=128, blank=True, null=True) # Changed to Branch
    Description = models.CharField(max_length=128, blank=True, null=True)
    IsTrialVersion = models.BooleanField(default=False)
    Edition = models.CharField(
        max_length=128, default="Standard", blank=True, null=True
    ) # Changed to Branch
    Permission = models.CharField(max_length=128, default="3", blank=True, null=True) # may be not need this column Nashid
    IsPosUser = models.BooleanField(default=False) # Changed to Branch
    EnableZatca = models.BooleanField(default=False) # Changed to Branch
    financial_year_period = models.CharField(max_length=500, blank=True, null=True) # Changed to Branch
    IsTest = models.BooleanField(default=False)
    NoOfRassassyUsers = models.IntegerField(default=0) # added by anirudh
    Stotage = models.PositiveIntegerField(default=1024) # 1024 MB by default
    class Meta:
        db_table = "companySettings_companySettings"
        verbose_name = _("companySettings")
        verbose_name_plural = _("companySettingss")
        ordering = ("-CompanyName", "CreatedDate")

    def __unicode__(self):
        return str(self.CompanyName)

class SalesMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CompanyID = models.ForeignKey(
        "CompanySettings", on_delete=models.CASCADE, blank=True, null=True, db_index=True
    )
    # LoyaltyCustomerID = models.ForeignKey(
    #     "brands.LoyaltyCustomer", on_delete=models.PROTECT, blank=True, null=True
    # )
    SalesMasterID = models.BigIntegerField()
    BranchID = models.BigIntegerField()
    Action = models.CharField(max_length=128, blank=True, null=True, default="A")
    VoucherNo = models.CharField(max_length=128, blank=True, null=True)
    Date = models.DateField(blank=True, null=True)
    CreditPeriod = models.BigIntegerField(blank=True, null=True)
    LedgerID = models.BigIntegerField(blank=True, null=True)
    PriceCategoryID = models.BigIntegerField(blank=True, null=True)
    EmployeeID = models.BigIntegerField(blank=True, null=True)
    SalesAccount = models.BigIntegerField(blank=True, null=True)
    CustomerName = models.CharField(max_length=128, blank=True, null=True)
    Address1 = models.CharField(max_length=150, blank=True, null=True)
    Address2 = models.CharField(max_length=150, blank=True, null=True)
    Address3 = models.CharField(max_length=150, blank=True, null=True)
    Notes = models.TextField(blank=True, null=True)
    FinacialYearID = models.BigIntegerField(blank=True, null=True)
    TotalGrossAmt = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    AddlDiscPercent = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    AddlDiscAmt = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TotalDiscount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TotalTax = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TotalTaxableAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )  # LineExtensionAmount (each line (gross amount - discount))
    NetTotal = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    AdditionalCost = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    GrandTotal = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    RoundOff = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    CashReceived = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    CashAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    BankAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    WarehouseID = models.BigIntegerField(blank=True, null=True)
    SeatNumber = models.CharField(max_length=128, blank=True, null=True)
    NoOfGuests = models.BigIntegerField(blank=True, null=True)
    INOUT = models.BooleanField(default=False)
    TokenNumber = models.BigIntegerField(blank=True, null=True)
    CardTypeID = models.BigIntegerField(blank=True, null=True)
    CardNumber = models.CharField(max_length=128, blank=True, null=True)
    IsActive = models.BooleanField(default=True)
    IsPosted = models.BooleanField(default=False)
    SalesType = models.CharField(max_length=150, blank=True, null=True)
    CreatedDate = models.DateTimeField(blank=True, null=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUserID = models.BigIntegerField(blank=True, null=True)
    UpdatedUserID = models.BigIntegerField(blank=True, null=True)
    TaxID = models.BigIntegerField(blank=True, null=True)
    TaxType = models.CharField(max_length=128, blank=True, null=True)
    BillDiscPercent = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    BillDiscAmt = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    VATAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    ExciseTaxAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    SGSTAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    CGSTAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    IGSTAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TAX1Amount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TAX2Amount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TAX3Amount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    KFCAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    Balance = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TransactionTypeID = models.BigIntegerField(blank=True, null=True)
    OldLedgerBalance = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    CashID = models.BigIntegerField(blank=True, null=True)
    BankID = models.BigIntegerField(blank=True, null=True)
    ShippingCharge = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    shipping_tax_amount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    TaxTypeID = models.CharField(max_length=128, blank=True, null=True)
    SAC = models.CharField(max_length=128, blank=True, null=True)
    SalesTax = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    Country_of_Supply = models.CharField(max_length=128, blank=True, null=True)
    State_of_Supply = models.CharField(max_length=128, blank=True, null=True)
    GST_Treatment = models.CharField(max_length=128, blank=True, null=True)
    VAT_Treatment = models.CharField(max_length=128, blank=True, null=True)
    Status = models.CharField(max_length=128, blank=True, null=True, default="Invoiced")
    DeliveryManID = models.BigIntegerField(blank=True, null=True)  # for POS save Employee as Delivery man
    # StaffID = models.CharField(max_length=50,blank=True, null=True)
    TableID = models.BigIntegerField(blank=True, null=True)
    # Table = models.ForeignKey(
    #     "brands.POS_Table", on_delete=models.PROTECT, blank=True, null=True
    # )
    # ShippingAddress = models.ForeignKey(
    #     "brands.UserAdrress",
    #     related_name="ShippingAddress",
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True,
    # )
    # BillingAddress = models.ForeignKey(
    #     "brands.UserAdrress",
    #     related_name="BillingAddress",
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True,
    # )
    TaxTaxableAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    NonTaxTaxableAmount = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )
    OrderNo = models.CharField(max_length=128, blank=True, null=True)
    DiscoundBeforeTax = models.BooleanField(default=False, blank=True, null=True)
    is_manual_roundoff = models.BooleanField(default=False)
    Type = models.CharField(max_length=128, blank=True, null=True)  # Dining,TakeAway,Online,Car
    DeviceCode = models.CharField(max_length=128, blank=True, null=True)
    DeliveryDate = models.DateField(blank=True, null=True)

    RefferenceBillNo = models.CharField(max_length=128, blank=True, null=True)
    RefferenceBillDate = models.DateField(blank=True, null=True)
    # onlinePlatform = models.ForeignKey("brands.PosOnlinePlatform", on_delete=models.PROTECT, blank=True, null=True,
    #                                    default=None)

    ShippingTaxID = models.BigIntegerField(default=None, blank=True, null=True)

    IsNewSale = models.BooleanField(default=False, blank=True, null=True)

    # Einvoice
    # zatca_transaction = models.ForeignKey("brands.ZatcaTransaction", on_delete=models.PROTECT, blank=True, null=True,
    #                                       default=None)
    # Table_split = models.ForeignKey(
    #     "brands.POS_Split_Table", on_delete=models.PROTECT, blank=True, null=True
    # )
    BillDiscTaxAmt = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)
    BillDiscTaxPerc = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)
    BillDiscTaxID = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)
    Phone = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = "salesMasters_salesMaster"
        verbose_name = _("salesMaster")
        verbose_name_plural = _("salesMasters")
        unique_together = (("CompanyID", "SalesMasterID"),)
        ordering = ("-SalesMasterID",)

    def __unicode__(self):
        return str(self.SalesMasterID)

    def save(self, *args, **kwargs):
        if not self.DeliveryDate:
            self.DeliveryDate = now().date()
        # if not self.SalesMasterID or self.SalesMasterID:
        #     last_obj = (SalesMaster.objects.filter(CompanyID=self.CompanyID,).order_by("-SalesMasterID").first())
        #     self.SalesMasterID = (last_obj.SalesMasterID if last_obj else 0) + 1

        super(SalesMaster, self).save(*args, **kwargs)


# Create your models here.
class Test(models.Model):
    id = models.AutoField(primary_key=True, default=uuid.uuid4())
    voucher_no = models.CharField(max_length=50, default="")
    voucher_date = models.DateField(auto_now_add=True)


class GeneralSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CompanyID = models.ForeignKey(
        "CompanySettings", on_delete=models.CASCADE, blank=True, null=True, db_index=True
    )
    GeneralSettingsID = models.BigIntegerField()
    BranchID = models.BigIntegerField()
    GroupName = models.CharField(max_length=150, blank=True, null=True, db_index=True)
    SettingsType = models.CharField(max_length=150, blank=True, null=True)
    SettingsValue = models.CharField(max_length=150, blank=True, null=True)
    Action = models.CharField(max_length=150, blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUserID = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = "generalSettings_generalSettings"
        verbose_name = _("generalSettings")
        verbose_name_plural = _("generalSettingss")
        ordering = ("-GeneralSettingsID", "CreatedDate")
        unique_together = (("CompanyID", "GeneralSettingsID", "BranchID"),)

    def __unicode__(self):
        return str(self.GeneralSettingsID)