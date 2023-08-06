from datetime import datetime
from datetime import timedelta
import json, re, os, sys, requests
import pandas as pd

class MimeTypes():
    GAPPS_AUDIO = "application/vnd.google-apps.audio"
    GAPPS_DOCUMENT = "application/vnd.google-apps.document"
    GAPPS_DRAWING = "application/vnd.google-apps.drawing"
    GAPPS_DRIVE = "application/vnd.google-apps.drive"
    GAPPS_FILE = "application/vnd.google-apps.file"
    GAPPS_FOLDER = "application/vnd.google-apps.folder"
    GAPPS_FORM = "application/vnd.google-apps.form"
    GAPPS_FUSIONTABLE = "application/vnd.google-apps.fusiontable"
    GAPPS_JAM = "application/vnd.google-apps.jam"
    GAPPS_JSON = "application/vnd.google-apps.script+json"
    GAPPS_MAP = "application/vnd.google-apps.map"
    GAPPS_PHOTO = "application/vnd.google-apps.photo"
    GAPPS_PRESENTATION = "application/vnd.google-apps.presentation"
    GAPPS_SCRIPT = "application/vnd.google-apps.script"
    GAPPS_SHORTCUT = "application/vnd.google-apps.shortcut"
    GAPPS_SITE = "application/vnd.google-apps.site"
    GAPPS_SPREADSHEET = "application/vnd.google-apps.spreadsheet"
    GAPPS_UNKNOWN = "application/vnd.google-apps.unknown"
    GAPPS_VIDE = "application/vnd.google-apps.vide"
    APP_ARJ = "application/arj"
    APP_CAB = "application/cab"
    APP_DOCUMENT = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    APP_EPUB_ZIP = "application/epub+zip"
    APP_EXCEL = "application/vnd.ms-excel"
    APP_FLASH = "application/x-shockwave-flash"
    APP_MSWORD = "application/msword"
    APP_OCTET_STREAM = "application/octet-stream"
    APP_PDF = "application/pdf"
    APP_PHP = "application/x-httpd-php"
    APP_RAR = "application/rar"
    APP_OFFICE_PRESENTATION = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    APP_OFFICE_SHEET = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    APP_OPEN_DOC_PRESENTATION = "application/vnd.oasis.opendocument.presentation"
    APP_OPEN_DOC_SPREADSHEET = "application/vnd.oasis.opendocument.spreadsheet"
    APP_OPEN_DOC_TEXT = "application/vnd.oasis.opendocument.text"
    APP_RTF = "application/rtf"
    APP_TAR = "application/tar"
    APP_ZIP = "application/zip"
    TEXT_CSV = "text/csv"
    TEXT_HTML = "text/html"
    TEXT_JS = "text/js"
    TEXT_PLAIN = "text/plain"
    TEXT_TAB_SEPARATED_VALUES = "text/tab-separated-values"
    TEXT_XML = "text/xml"
    IMAGE_BMP = "image/bmp"
    IMAGE_GIF = "image/gif"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_PNG = "image/png"
    IMAGE_SVG_XML = "image/svg+xml"
    AUDIO_MPEG = "audio/mpeg"

    def __init__(self):
        pass

class GSheetsApiMajorDimension():
    ROWS = 'ROWS'
    COLUMNS = 'COLUMNS'

class GSheetsApiValueInputOption():
    RAW = 'RAW'
    USER_ENTERED = 'USER_ENTERED'

class GSheetsApiValueRenderOption():
    FORMATTED_VALUE = 'FORMATTED_VALUE'
    UNFORMATTED_VALUE = 'UNFORMATTED_VALUE'
    FORMULA = 'FORMULA'

class GSheetsApiDateTimeRenderOption():
    SERIAL_NUMBER = 'SERIAL_NUMBER'
    FORMATTED_STRING = 'FORMATTED_STRING'
class GSheetsApiDefinedValues():
    major_dimension = GSheetsApiMajorDimension()
    value_input_option = GSheetsApiValueInputOption()
    value_render_option = GSheetsApiValueRenderOption()
    date_time_render_option = GSheetsApiDateTimeRenderOption()
    
class Helper():
    def __init__(self):
        super().__init__()

    def getColors(self, file_ntc='downloads/ntc.txt', file_colors='utils/colors.json', buf=7):
        ntc_exists = os.path.exists(file_ntc)

        if ntc_exists:
            lastUpdate = datetime.fromtimestamp(os.stat(file_colors).st_mtime)
            today = datetime.now()
            if today - lastUpdate > timedelta(days = buf):
                os.system(f'curl http://chir.ag/projects/ntc/ntc.js --output {file_ntc}')
        else:
            os.system(f'curl http://chir.ag/projects/ntc/ntc.js --output {file_ntc}')

        ntc_exists = os.path.exists(file_ntc)
        if ntc_exists:
            with open(file_ntc) as f:
                text = f.read()
                matches = re.search(r'(names:\s*[[](\s*([[][^[]*[\]])(,\s*[[][^[]*[\]])*)?\s*[\]])', text)
            if matches:
                names = matches[0]
                names = re.sub(r'^names', '\"names\"', names)
                names = eval(f'{{{names}}}')
                colors = dict()
                for color in names['names']:
                    colors[color[1].lower()] = color[0].lower()
                with open(file_colors, 'w') as f:
                    json.dump(colors, f)

        colors_exists = os.path.exists(file_colors)
        if colors_exists:
            with open(file_colors, 'r') as f:
                colors = json.load(f)
            return colors
        else:
            return ['#000000', '#434343', '#666666', '#999999', '#cccccc', '#efefef', '#f3f3f3', '#ffffff', '#fb4c2f', '#ffad47', '#fad165', '#16a766', '#43d692', '#4a86e8', '#a479e2', '#f691b3', '#f6c5be', '#ffe6c7', '#fef1d1', '#b9e4d0', '#c6f3de', '#c9daf8', '#e4d7f5', '#fcdee8', '#efa093', '#ffd6a2', '#fce8b3', '#89d3b2', '#a0eac9', '#a4c2f4', '#d0bcf1', '#fbc8d9', '#e66550', '#ffbc6b', '#fcda83', '#44b984', '#68dfa9', '#6d9eeb', '#b694e8', '#f7a7c0', '#cc3a21', '#eaa041', '#f2c960', '#149e60', '#3dc789', '#3c78d8', '#8e63ce', '#e07798', '#ac2b16', '#cf8933', '#d5ae49', '#0b804b', '#2a9c68', '#285bac', '#653e9b', '#b65775', '#822111', '#a46a21', '#aa8831', '#076239', '#1a764d', '#1c4587', '#41236d', '#83334c #464646', '#e7e7e7', '#0d3472', '#b6cff5', '#0d3b44', '#98d7e4', '#3d188e', '#e3d7ff', '#711a36', '#fbd3e0', '#8a1c0a', '#f2b2a8', '#7a2e0b', '#ffc8af', '#7a4706', '#ffdeb5', '#594c05', '#fbe983', '#684e07', '#fdedc1', '#0b4f30', '#b3efd3', '#04502e', '#a2dcc1', '#c2c2c2', '#4986e7', '#2da2bb', '#b99aff', '#994a64', '#f691b2', '#ff7537', '#ffad46', '#662e37', '#ebdbde', '#cca6ac', '#094228', '#42d692', '#16a765']

    def possibleGmailLabelColors(self):
        return ['#000000', '#434343', '#666666', '#999999', '#cccccc', '#efefef', '#f3f3f3', '#ffffff', '#fb4c2f', '#ffad47', '#fad165', '#16a766', '#43d692', '#4a86e8', '#a479e2', '#f691b3', '#f6c5be', '#ffe6c7', '#fef1d1', '#b9e4d0', '#c6f3de', '#c9daf8', '#e4d7f5', '#fcdee8', '#efa093', '#ffd6a2', '#fce8b3', '#89d3b2', '#a0eac9', '#a4c2f4', '#d0bcf1', '#fbc8d9', '#e66550', '#ffbc6b', '#fcda83', '#44b984', '#68dfa9', '#6d9eeb', '#b694e8', '#f7a7c0', '#cc3a21', '#eaa041', '#f2c960', '#149e60', '#3dc789', '#3c78d8', '#8e63ce', '#e07798', '#ac2b16', '#cf8933', '#d5ae49', '#0b804b', '#2a9c68', '#285bac', '#653e9b', '#b65775', '#822111', '#a46a21', '#aa8831', '#076239', '#1a764d', '#1c4587', '#41236d', '#83334c #464646', '#e7e7e7', '#0d3472', '#b6cff5', '#0d3b44', '#98d7e4', '#3d188e', '#e3d7ff', '#711a36', '#fbd3e0', '#8a1c0a', '#f2b2a8', '#7a2e0b', '#ffc8af', '#7a4706', '#ffdeb5', '#594c05', '#fbe983', '#684e07', '#fdedc1', '#0b4f30', '#b3efd3', '#04502e', '#a2dcc1', '#c2c2c2', '#4986e7', '#2da2bb', '#b99aff', '#994a64', '#f691b2', '#ff7537', '#ffad46', '#662e37', '#ebdbde', '#cca6ac', '#094228', '#42d692', '#16a765']

    def isValidGmailLabelColor(self, color):
        count = self.possibleGmailLabelColors().count(color)
        return True if count > 0 else False

    def getExcelFromUrl(self, url, dest, convertToCsv=False):
        req = requests.get(url)
        with open(dest, 'wb') as f:
            f.write(req.content)
        
        if convertToCsv:
            df = pd.read_excel(dest)
            newDest = re.sub(r'[.](xls|xlsx|xlsm|xlsb|odf|ods|odt)$', '.csv', dest)
            df.to_csv(newDest)
            os.remove(dest)
