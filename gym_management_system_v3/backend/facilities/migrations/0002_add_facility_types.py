from django.db import migrations

def add_facility_types(apps, schema_editor):
    FacilityType = apps.get_model('facilities', 'FacilityType')
    
    # 添加场馆类型数据
    types = [
        {
            'type_name': '篮球场',
            'icon': 'el-icon-basketball',
            'description': '标准篮球场',
            'sort_order': 1,
            'is_active': True
        },
        {
            'type_name': '羽毛球场',
            'icon': 'el-icon-basketball',
            'description': '标准羽毛球场',
            'sort_order': 2,
            'is_active': True
        },
        {
            'type_name': '网球场',
            'icon': 'el-icon-basketball',
            'description': '标准网球场',
            'sort_order': 3,
            'is_active': True
        },
        {
            'type_name': '游泳池',
            'icon': 'el-icon-basketball',
            'description': '标准游泳池',
            'sort_order': 4,
            'is_active': True
        }
    ]
    
    for type_data in types:
        FacilityType.objects.create(**type_data)

def remove_facility_types(apps, schema_editor):
    FacilityType = apps.get_model('facilities', 'FacilityType')
    FacilityType.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('facilities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_facility_types, remove_facility_types),
    ] 