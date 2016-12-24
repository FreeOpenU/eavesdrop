import re
import zlib

def HTTPHeaders(http_payload):
    try:
        # isolate headers
        headers_raw = http_payload[:http_payload.index("\r\n\r\n") + 2]
        regex = ur"(?P&lt;'name&gt;.*?): (?P&lt;value&gt;.*?)\r\n"
        headers = dict(re.findall(regex, headers_raw, re.UNICODE))
        return headers
    except:
        return None
    if 'Content-Type' not in headers:
        return None
    return headers

def extractText(headers, http_payload):
        text = None
        try:
            if 'text' in headers['Content-Type']:
                text = http_payload[http_payload.index("\r\n\r\n")+4:]
                try:
                    if "Accept-Encoding" in headers.keys():
                        if headers['Accept-Encoding'] == "gzip":
                            text = zlib.decompress(text,  16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        text = zlib.decompress(text)
                except: pass
        except:
            return None
        return text
