__context__ = 'zero-doc'
__doc__ = 'Opens settings of CustomTools'

from pyrevit.userconfig import user_config
try:
	user_config.add_section('CustomToolsSettings')
except:
	pass
user_config.newsection.hooks_path = "value 2"
# user_config.newsection.get('property', default_value)
user_config.save_changes()

"""
hooks logging path
versions logging path
dashboards path
"""