from django.contrib import admin
from .models import Member, Uniform_Piece, Instrument

class MemberAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "vandal_number"]
    search_fields=["last_name", "vandal_number"]

class UniformAdmin(admin.ModelAdmin):
    list_display = ["clothing_type", "size", "clothing_id"]
    list_filter = ["clothing_type"]
    search_fields = ["clothing_type", "clothing_id"]

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ["instrument_type", "instrument_id"]
    list_filter = ["instrument_type"]
    search_fields = ["instrument_type", "instrument_id"]

admin.site.register(Member, MemberAdmin)
admin.site.register(Uniform_Piece, UniformAdmin)
admin.site.register(Instrument, InstrumentAdmin)

