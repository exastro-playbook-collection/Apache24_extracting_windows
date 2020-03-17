import os
import json
import sys
import re

# main process
args = sys.argv
if (len(args) < 2):
    sys.exit(1)
path = args[1]
if(path[-1:] == "/"):
    path = path[:-1]

result_dict = {}

input_parameter_path = path + '/' + 'input_parameter_install'
with open(input_parameter_path) as file_object:
    lines = file_object.readlines()
for line in lines:
    if 'VAR_Apache24_WIN_path' in line:
        result_dict['VAR_Apache24_WIN_path'] = line.split(':',1)[1].strip()

filename1 = path + '/command/0/stdout.txt'
filename2 = path + '/command/1/stdout.txt'
filename3 = path + '/command/2/stdout.txt'
filename4 = path + '/command/3/stdout.txt'
filename5 = path + '/command/4/stdout.txt'

log_config_module_flg = False
logio_module_flg = False

result_dict['VAR_Apache24_WIN_ServiceName'] = "Apache2.4"
result_dict['VAR_Apache24_WIN_Http'] = True
# paramete(httpd.conf)
http_list_dict={
    'VAR_Apache24_WIN_Http_ServerAdmin':'ServerAdmin',
    'VAR_Apache24_WIN_Http_ServerName':'ServerName',
    'VAR_Apache24_WIN_Http_DirectoryIndex':'DirectoryIndex',
    'VAR_Apache24_WIN_Http_TypesConfig':'TypesConfig',
    'VAR_Apache24_WIN_Http_AddDefaultCharset':'AddDefaultCharset',
    'VAR_Apache24_WIN_Http_MIMEMagicFile':'MIMEMagicFile',
    'VAR_Apache24_WIN_Http_LogLevel':'LogLevel',
    'VAR_Apache24_WIN_Http_CustomLog':'CustomLog',
    'VAR_Apache24_WIN_Http_EnableMMAP':'EnableMMAP',
    'VAR_Apache24_WIN_Http_EnableSendfile':'EnableSendfile'
    }

# paramete(httpd-default.conf)
default_list_dict={
    'VAR_Apache24_WIN_Default_ServerTokens':'ServerTokens',
    'VAR_Apache24_WIN_Default_KeepAlive':'KeepAlive',
    'VAR_Apache24_WIN_Default_UseCanonicalName':'UseCanonicalName',
    'VAR_Apache24_WIN_Default_AccessFileName':'AccessFileName',
    'VAR_Apache24_WIN_Default_HostnameLookups':'HostnameLookups',
    'VAR_Apache24_WIN_Default_ServerSignature':'ServerSignature',
    'VAR_Apache24_WIN_Default_RequestReadTimeout':'RequestReadTimeout'
    }

# paramete(httpd-info.conf)
info_list_dict={
    'VAR_Apache24_WIN_Info_ExtendedStatus':'ExtendedStatus'
    }

# paramete(proxy.conf)
proxy_list_dict={
    'VAR_Apache24_WIN_ProxyBadHeader':'ProxyBadHeader',
    'VAR_Apache24_WIN_ProxyBlock':'ProxyBlock',
    'VAR_Apache24_WIN_ProxyDomain':'ProxyDomain',
    'VAR_Apache24_WIN_ProxyErrorOverride':'ProxyErrorOverride',
    'VAR_Apache24_WIN_ProxyPassInterpolateEnv':'ProxyPassInterpolateEnv',
    'VAR_Apache24_WIN_ProxyPreserveHost':'ProxyPreserveHost',
    'VAR_Apache24_WIN_ProxyStatus':'ProxyStatus',
    'VAR_Apache24_WIN_ProxyVia':'ProxyVia',
    'VAR_Apache24_WIN_ProxyAddHeaders':'ProxyAddHeaders',
    'VAR_Apache24_WIN_ProxyPassInherit':'ProxyPassInherit',
    'VAR_Apache24_WIN_ProxySourceAddress':'ProxySourceAddress'
    }

default_file_flg = False
info_file_flg = False
mpm_file_flg = False
proxy_file_flg = False

# For parameter in file
def genPara( para_name, content_name, line ):
    if (re.match( '\s*' + content_name + '\s+(.*)', line) != None):
        temp_var = line.rsplit(content_name, 1)[1]
        result_dict[para_name] = temp_var.strip()

if os.path.isfile(filename1):
    fo = open(filename1)
    alllines = fo.readlines()
    for line in alllines:
        line = line.strip()
        for temp in http_list_dict.keys():
            genPara( temp, http_list_dict[temp], line )
        if (re.match( '\s*' + "ServerRoot" + '\s+(.*)', line) != None):
            strServerRoot = line.rsplit('ServerRoot', 1)[1]
            result_dict['VAR_Apache24_WIN_Http_ServerRoot'] = eval(strServerRoot.strip())
        if (re.match( '\s*' + "DocumentRoot" + '\s+(.*)', line) != None):
            strDocumentRoot = line.rsplit('DocumentRoot', 1)[1]
            result_dict['VAR_Apache24_WIN_Http_DocumentRoot'] = eval(strDocumentRoot.strip())
        if (re.match( '\s*' + "ErrorLog" + '\s+(.*)', line) != None):
            strErrorLog = line.rsplit('ErrorLog', 1)[1]
            result_dict['VAR_Apache24_WIN_Http_ErrorLog'] = eval(strErrorLog.strip())
        if (re.match( '\s*' + "Listen" + '\s+(.*)', line) != None):
            strListen = line.rsplit('Listen', 1)[1]
            if strListen is not None:
                result_dict['VAR_Apache24_WIN_Http_Listen'] = int(strListen.strip())
        if '<IfModule log_config_module>' in line:
            log_config_module_flg = True
        if log_config_module_flg is True:
            if line.strip().startswith('LogFormat') and line.strip().endswith('combined'):
                strLogFormat = line.rsplit('LogFormat', 1)[1]
                result_dict['VAR_Apache24_WIN_Http_LogFormat'] = strLogFormat.strip()
                log_config_module_flg = False
        if '<IfModule logio_module>' in line:
            logio_module_flg = True
        if logio_module_flg is True:
            if line.strip().startswith('LogFormat') and line.strip().endswith('combinedio'):
                strLogFormatIo = line.rsplit('LogFormat', 1)[1]
                result_dict['VAR_Apache24_WIN_Http_LogFormat_IO'] = strLogFormatIo.strip()
                logio_module_flg = False
        if (re.match( '\s*Include\s+conf/extra/httpd-default.conf\s*', line) != None):
            default_file_flg = True
        if (re.match( '\s*Include\s+conf/extra/httpd-info.conf\s*', line) != None):
            info_file_flg = True
        if (re.match( '\s*Include\s+conf/extra/httpd-mpm.conf\s*', line) != None):
            mpm_file_flg = True
        if (re.match( '\s*Include\s+conf/extra/proxy.conf\s*', line) != None):
            proxy_file_flg = True
    fo.close()

if default_file_flg is True:
    result_dict['VAR_Apache24_WIN_Default'] = True
    if os.path.isfile(filename2):
        fo = open(filename2)
        alllines = fo.readlines()
        for line in alllines:
            for temp in default_list_dict.keys():
                genPara( temp, default_list_dict[temp], line )
            if (re.match( '\s*' + "Timeout" + '\s+(.*)', line) != None):
                strTimeout = line.rsplit('Timeout', 1)[1]
                if strTimeout is not None:
                    result_dict['VAR_Apache24_WIN_Default_Timeout'] = int(strTimeout.strip())
            if (re.match( '\s*' + "MaxKeepAliveRequests" + '\s+(.*)', line) != None):
                strMaxKeepAliveRequests = line.rsplit('MaxKeepAliveRequests', 1)[1]
                if strMaxKeepAliveRequests is not None:
                    result_dict['VAR_Apache24_WIN_Default_MaxKeepAliveRequests'] = int(strMaxKeepAliveRequests.strip())
            if (re.match( '\s*' + "KeepAliveTimeout" + '\s+(.*)', line) != None):
                strKeepAliveTimeout = line.rsplit('KeepAliveTimeout', 1)[1]
                if strKeepAliveTimeout is not None:
                    result_dict['VAR_Apache24_WIN_Default_KeepAliveTimeout'] = int(strKeepAliveTimeout.strip())
        default_file_flg = False
        fo.close()

serverStatus_Location = ""
locationFlg = False
require_list = []
if info_file_flg is True:
    result_dict['VAR_Apache24_WIN_Info'] = True
    if os.path.isfile(filename3):
        fo = open(filename3)
        alllines = fo.readlines()
        for line in alllines:
            for temp in info_list_dict.keys():
                genPara( temp, info_list_dict[temp], line )
            if (re.match( '\s*' + "<Location" + '\s+(.*)', line) != None):
                temp_var = line.rsplit("<Location", 1)[1].strip()
                serverStatus_Location = temp_var[:-1]
            if line.strip().startswith('SetHandler server-status'):
                result_dict['VAR_Apache24_WIN_Info_ServerStatus'] = True
                result_dict['VAR_Apache24_WIN_Info_ServerStatus_Location'] = serverStatus_Location
                locationFlg = True
            if locationFlg is True:
                if line.strip().startswith('<RequireAny>') or line.strip().startswith('<RequireAll>'):
                    result_dict['VAR_Apache24_WIN_Info_ServerStatus_Require'] = line.strip()[1:-1]
                if (re.match( '\s*' + "Require" + '\s+(.*)', line) != None):
                    re_var = line.rsplit("Require", 1)[1]
                    require_list.append(re_var.strip())
            if line.strip().startswith('</Location>'):
                locationFlg = False
        result_dict['VAR_Apache24_WIN_Info_ServerStatus_RequireResource'] = require_list
        info_file_flg = False
        fo.close()

acceptFilter_list = []
if mpm_file_flg is True:
    result_dict['VAR_Apache24_WIN_MPM'] = True
    if os.path.isfile(filename4):
        fo = open(filename4)
        alllines = fo.readlines()
        for line in alllines:
            if (re.match( '\s*' + "ThreadsPerChild" + '\s+(.*)', line) != None):
                strThreadsPerChild = line.rsplit('ThreadsPerChild', 1)[1]
                if strThreadsPerChild is not None:
                    result_dict['VAR_Apache24_WIN_MPM_ThreadsPerChild'] = int(strThreadsPerChild.strip())
            if (re.match( '\s*' + "MaxConnectionsPerChild" + '\s+(.*)', line) != None):
                strMaxConnectionsPerChild = line.rsplit('MaxConnectionsPerChild', 1)[1]
                if strMaxConnectionsPerChild is not None:
                    result_dict['VAR_Apache24_WIN_MPM_MaxConnectionsPerChild'] = int(strMaxConnectionsPerChild.strip())
            if (re.match( '\s*' + "MaxMemFree" + '\s+(.*)', line) != None):
                strMaxMemFree = line.rsplit('MaxMemFree', 1)[1]
                if strMaxMemFree is not None:
                    result_dict['VAR_Apache24_WIN_MPM_MaxMemFree'] = int(strMaxMemFree.strip())
            if (re.match( '\s*' + "AcceptFilter" + '\s+(.*)', line) != None):
                ac_var = line.rsplit("AcceptFilter", 1)[1]
                acceptFilter_list.append(ac_var.strip())
        result_dict['VAR_Apache24_WIN_MPM_AcceptFilter'] = acceptFilter_list
        mpm_file_flg = False
        fo.close()

proxyPass_list = []
proxyPassReverse_list = []
proxyPassReverseCookieDomain_list = []
proxyPassReverseCookiePath_list = []
proxyPassMatch_list = []
proxySet_list = []
if proxy_file_flg is True:
    result_dict['VAR_Apache24_WIN_Proxy'] = True
    if os.path.isfile(filename5):
        fo = open(filename5)
        alllines = fo.readlines()
        for line in alllines:
            for temp in proxy_list_dict.keys():
                genPara( temp, proxy_list_dict[temp], line )
            if (re.match( '\s*' + "ProxyIOBufferSize" + '\s+(.*)', line) != None):
                strProxyIOBufferSize = line.rsplit('ProxyIOBufferSize', 1)[1]
                if strProxyIOBufferSize is not None:
                    result_dict['VAR_Apache24_WIN_ProxyIOBufferSize'] = int(strProxyIOBufferSize.strip())
            if (re.match( '\s*' + "ProxyMaxForwards" + '\s+(.*)', line) != None):
                strProxyMaxForwards = line.rsplit('ProxyMaxForwards', 1)[1]
                if strProxyMaxForwards is not None:
                    result_dict['VAR_Apache24_WIN_ProxyMaxForwards'] = int(strProxyMaxForwards.strip())
            if (re.match( '\s*' + "ProxyReceiveBufferSize" + '\s+(.*)', line) != None):
                strProxyReceiveBufferSize = line.rsplit('ProxyReceiveBufferSize', 1)[1]
                if strProxyReceiveBufferSize is not None:
                    result_dict['VAR_Apache24_WIN_ProxyReceiveBufferSize'] = int(strProxyReceiveBufferSize.strip())
            if (re.match( '\s*' + "ProxyTimeout" + '\s+(.*)', line) != None):
                strProxyTimeout = line.rsplit('ProxyTimeout', 1)[1]
                if strProxyTimeout is not None:
                    result_dict['VAR_Apache24_WIN_ProxyTimeout'] = int(strProxyTimeout.strip())
            if (re.match( '\s*' + "ProxyPass" + '\s+(.*)', line) != None):
                propa_var = line.rsplit("ProxyPass", 1)[1]
                proxyPass_list.append(propa_var.strip())
            if (re.match( '\s*' + "ProxyPassReverse" + '\s+(.*)', line) != None):
                propare_var = line.rsplit("ProxyPassReverse", 1)[1]
                proxyPassReverse_list.append(propare_var.strip())
            if (re.match( '\s*' + "ProxyPassReverseCookieDomain" + '\s+(.*)', line) != None):
                propareco_var = line.rsplit("ProxyPassReverseCookieDomain", 1)[1]
                proxyPassReverseCookieDomain_list.append(propareco_var.strip())
            if (re.match( '\s*' + "ProxyPassReverseCookiePath" + '\s+(.*)', line) != None):
                proparecopath_var = line.rsplit("ProxyPassReverseCookiePath", 1)[1]
                proxyPassReverseCookiePath_list.append(proparecopath_var.strip())
            if (re.match( '\s*' + "ProxyPassMatch" + '\s+(.*)', line) != None):
                propama_var = line.rsplit("ProxyPassMatch", 1)[1]
                proxyPassMatch_list.append(propama_var.strip())
            if (re.match( '\s*' + "ProxySet" + '\s+(.*)', line) != None):
                proSet_var = line.rsplit("ProxySet", 1)[1]
                proxySet_list.append(proSet_var.strip())
        result_dict['VAR_Apache24_WIN_ProxyPass'] = proxyPass_list
        result_dict['VAR_Apache24_WIN_ProxyPassReverse'] = proxyPassReverse_list
        result_dict['VAR_Apache24_WIN_ProxyPassReverseCookieDomain'] = proxyPassReverseCookieDomain_list
        result_dict['VAR_Apache24_WIN_ProxyPassReverseCookiePath'] = proxyPassReverseCookiePath_list
        result_dict['VAR_Apache24_WIN_ProxyPassMatch'] = proxyPassMatch_list
        result_dict['VAR_Apache24_WIN_ProxySet'] = proxySet_list
        proxy_file_flg = False
        fo.close()

print (json.dumps(result_dict))