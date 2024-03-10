from odoo import api, fields, models
from odoo.exceptions import ValidationError
import datetime
import time


class Lead(models.Model):
    _inherit = 'crm.lead'

    business_name = fields.Char("Business Name", required=False)
    client_category = fields.Selection(selection=[('restaurant', 'مطعم'), 
                                                  ('cafe', 'كافيه'),
                                                  ('restaurant_cafe', 'مطعم وكافيه'),
                                                  ('coffee', 'قهوة'),
                                                  ('hotel', 'فندق'),
                                                  ('trading', 'شركة توريدات'),
                                                  ('bakery', 'مخبوزات'),
                                                  ('sweet', 'حلواني'),], string="Client Category", required=False)
    restaurant_category = fields.Many2one('restaurant.category', required=False)
    client_type = fields.Many2one('client.type', string="Client Place Type", required=False)
    contact_person = fields.Char(string='Contact Person', required=False)
    job_title = fields.Many2one('job.title', string='Job Title', required=False)
    gender = fields.Selection(selection=[('male', 'ذكر'), ('female', 'أنثي')], string='Gender')
    national_id = fields.Char(string='National ID', size=14)

    # @api.constrains('national_id')
    # def _check_national_id_length(self):
    #     for record in self:
    #         if record.national_id and len(record.national_id) != 14:
    #             raise ValidationError("Phone number must be 14 characters long.")

    # phone = fields.Char(unaccent=False, required=False, default='01', size=11, store=True)

    # @api.constrains('phone')
    # def _check_phone_length(self):
    #     for record in self:
    #         if record.phone and len(record.phone) != 11:
    #             raise ValidationError("Phone number must be 11 characters long.")

    sales_person = fields.Many2one('res.users', string='Sales Person')
    discount = fields.Float(string='Discount', digits=(10, 2))
    receipt_start_time = fields.Datetime(string='Receipt Start Time', required=False)
    receipt_end_time = fields.Datetime(string='Receipt End Time', required=False)
    # mobile = fields.Char(unaccent=False, required=False, default='01', size=11)
    vendor = fields.Many2one('vendor.type', string='Vendor', required=False)
    sales_channel = fields.Many2one('sales.channel', string='Sales Channel', required=False)
    street = fields.Char('Street', compute='_compute_partner_address_values', readonly=False, store=True,
                         required=False)
    street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=False, store=True)
    zip = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=False, store=True)
    city_id = fields.Many2one('client.city')
    payment_type = fields.Selection(selection=[('cash', 'Cash'), ('postpaid', 'Postpaid')], string='Payment Type',
                                    required=False)

    # state_id = fields.Many2one(
    #     "res.country.state", string='Government',
    #     compute='_compute_partner_address_values', readonly=False, store=True,
    #     domain="[('country_id', '=?', country_id)]")
    # country_id = fields.Many2one(
    #     'res.country', string='Country',
    #     compute='_compute_partner_address_values', readonly=False, store=True)

    @api.depends('partner_id')
    def _compute_partner_address_values(self):
        """ Sync all or none of address fields """
        for lead in self:
            lead.update(lead._prepare_address_values_from_partner(lead.partner_id))


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # is_customer = fields.Boolean("Customer")
    # is_vendor = fields.Boolean("Vendor")
    # client_id = fields.Char("Client Seq")

    # @api.model
    # def create(self, values):
    #     partner = super(ResPartner, self).create(values)
    #
    #     if partner.is_customer:
    #         seq = self.env['ir.sequence'].next_by_code('customer.serial')
    #         partner.write({'client_id': seq})
    #     elif partner.is_vendor:
    #         seq = self.env['ir.sequence'].next_by_code('vendor.serial')
    #         partner.write({'client_id': seq})
    #
    #     return partner

    ar_client_name_ar = fields.Char("Arabic Name", required=False)
    en_client_name_en = fields.Char("English Name", required=False)
    business_name = fields.Char("Business Name", required=False)
    # client_business_type = fields.Selection(selection=[('individual', 'Individual'), ('commercial', 'Commercial')],
    #                                         string='Client Business Type', required=False)
    client_category = fields.Selection(selection=[('restaurant', 'مطعم'), 
                                                  ('cafe', 'كافيه'),
                                                  ('restaurant_cafe', 'مطعم وكافيه'),
                                                  ('coffee', 'قهوة'),
                                                  ('hotel', 'فندق'),
                                                  ('trading', 'شركة توريدات'),
                                                  ('bakery', 'مخبوزات'),
                                                  ('sweet', 'حلواني'),], string="Client Category", required=False)
    restaurant_category = fields.Many2one('restaurant.category', string="Client Category", required=False)
    client_type = fields.Many2one('client.type', string="Client Place Type", required=False)
    client_status = fields.Selection(
        selection=[('active', 'نشط'), ('inactive', 'غير نشط'), ('suspended', 'معلق'), ('churn', 'متوقف')],
        string='Client Status', required=False, help='يتم منع عمل فاتورة او امر بيع او عرض سعر في حالة انه (معلق - قائمة سوداء)')
    churn_suspend_reason = fields.Char(string="Churn Suspend Reason")

    contact_person = fields.Char(string='Contact Person', required=False)
    job_title = fields.Many2one('job.title', string='Job Title', required=False)
    # phone = fields.Char(unaccent=False, required=False, default='01', size=11, store=True)
    management_address = fields.Char("Management Address", required=False)
    sales_person = fields.Many2one('res.users', string='Sales Person', help='مين اللي جاب العميل')

    # @api.constrains('phone')
    # def _check_phone_length(self):
    #     for record in self:
    #         if record.phone and len(record.phone) != 11:
    #             raise ValidationError("Phone number must be 11 characters long.")

    mobile = fields.Char(unaccent=False, required=False, default='+201', size=13)
    # # phone1 = fields.Char(string='Phone 1', required=True, size=11)
    # # phone2 = fields.Char(string='Phone 2', size=11)
    email = fields.Char(string='Email')
    # # address = fields.Text(string='Address', required=True)
    google_map_link = fields.Char(string='Google Map Link', required=False,
                                  help='Should start with "https://maps.app.goo.gl/"')

    # @api.constrains('google_map_link')
    # def _check_google_map_link(self):
    #     for record in self:
    #         if not record.google_map_link.startswith('https://maps.app.goo.gl/') or len(record.google_map_link) == len(
    #                 'https://maps.app.goo.gl/'):
    #             raise ValidationError(
    #                 "Invalid Google Map Link. It should start with 'https://maps.app.goo.gl/' and include additional characters.")

    coordinates = fields.Char(string='Coordinates', required=False, help='Format: "30.0597076,31.2242059"')
    country_id = fields.Many2one('res.country', string='Country', required=False)
    state_id = fields.Many2one('res.country.state', string='Government', domain=[('country_id', '=', 65)])

    birth_date = fields.Date(string='Birth Date')
    business_anniversary = fields.Date(string='Business Anniversary')
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female')], string='Gender')
    payment_type = fields.Selection(selection=[('cash', 'كاش'), ('postpaid', 'اجل')], string='Payment Type',
                                    required=False)
    credit_limit_amount = fields.Float(string='Credit Limit Amount', digits=(10, 2))
    credit_limit_period_in_days = fields.Integer(string='Credit Limit Period (Days)')
    national_id = fields.Char(string='National ID', size=14)
    city_id = fields.Many2one('client.city')

    # @api.constrains('national_id')
    # def _check_national_id_length(self):
    #     for record in self:
    #         if record.national_id and len(record.national_id) != 14:
    #             raise ValidationError("Phone number must be 14 characters long.")

    discount = fields.Float(string='Discount', digits=(10, 2))

    telesales = fields.Many2one('res.users', string='Telesales', required=False, help='مين اللي بيتابع العميل بالتيلفون وبيعمله عروض اسعار')
    sales_support = fields.Many2one('sales.support', string='Sales Support', required=False)
    # receipt_start_time = fields.Datetime(string='Receipt Start Time')
    receipt_start_time = fields.Datetime()
    receipt_end_time = fields.Datetime()
    # receipt_end_time = fields.Datetime(string='Receipt End Time', required=False)
    vendor = fields.Many2one('vendor.type', string='Vendor', required=False)
    sales_channel = fields.Many2one('sales.channel', string='Sales Channel', required=False)
    telesales_support = fields.Many2one('res.users', string='Telesales Support', required=False, help='مين اللي شغل العميل')
    onground_support = fields.Many2one('res.users', required=False, help='مين بيتابع العميل على الارض')
    client_id = fields.Char(string="Serial Number", readonly=True, copy=False, default="/")
    area_id = fields.Many2one('area', string='المنطقة')
    
    
    # @api.onchange('state_id')
    # def onchange_state_id(self):
    #     if self.state_id:
    #         # Filter areas based on the selected state
    #         areas = self.env['your.area].search([('state_id', '=', self.state_id.id)])
    #         domain = {'area': [('id', 'in', areas.ids)]}
    #     else:
    #         # If no state selected, show all areas
    #         domain = {'area': []}

    #     return {'domain': domain}

    @api.model
    def create(self, values):
        if not values.get('ref'):
            values['ref'] = values.get('ref', 'Generated Automatic')
        return super(ResPartner, self).create(values)
        
    # @api.model
    # def create(self, vals):
    #     partner_type = self._context.get('res_partner_search_mode')

    #     if partner_type == 'customer':
    #         vals['ref'] = self.env['ir.sequence'].next_by_code('customer.number')

    #     return super(ResPartner, self).create(vals)


class Area(models.Model):
    _name = 'area'

    name = fields.Char("name")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                              )
    # country_id = fields.Many2one('res.country', string='Country', ondelete='restrict', default=)
    

class ClientCategory(models.Model):
    _name = 'client.category'

    name = fields.Char("name")


class ClientCity(models.Model):
    _name = 'client.city'

    name = fields.Char("name")


class RestaurantCategory(models.Model):
    _name = 'restaurant.category'

    name = fields.Char("name")


class ClientType(models.Model):
    _name = 'client.type'

    name = fields.Char("name")


class JobTitle(models.Model):
    _name = 'job.title'

    name = fields.Char("name")


class AreaType(models.Model):
    _name = 'area.type'

    name = fields.Char("name")


class TeleSales(models.Model):
    _name = 'tele.sales'

    name = fields.Char("name")


class SalesSupport(models.Model):
    _name = 'sales.support'

    name = fields.Char("name")


class VendorType(models.Model):
    _name = 'vendor.type'

    name = fields.Char("name")


class SalesChannel(models.Model):
    _name = 'sales.channel'

    name = fields.Char("name")


class TelesalesSupport(models.Model):
    _name = 'telesales.support'

    name = fields.Char("name")


class OngroundSupport(models.Model):
    _name = 'onground.support'

    name = fields.Char("name")
