import sys
import xbmcgui
import xbmcplugin
import requests

addon_handle = int(sys.argv[1])

xbmcplugin.setContent(addon_handle, 'audio')

try:
    r = requests.get('http://ponyvillelive.com/api/station/list/category/audio')
except ConnectionError:
    xbmcgui.Dialog().ok('Error', 'Connection Error')
#except HTTPError:
#    xbmcgui.Dialog().ok('Status Code', str(r.status_code))
#except RequestException:
#    xbmcgui.Dialog().ok('Error', 'Request Failed')

if r.status_code != 200:
    xbmcgui.Dialog().ok('Status Code', str(r.status_code))

data = r.json()
result = data['result']

for index in range(len(result)):
    station = result[index]
    li = xbmcgui.ListItem(station['name'], station['genre'], iconImage=station['image_url'], thumbnailImage=station['image_url'])
    li.setInfo('music',{'count':station['id'], 'genre':station['genre']})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=station['stream_url'], listitem=li, totalItems=len(result))


xbmcplugin.endOfDirectory(addon_handle)