from io import BytesIO
from bs4 import BeautifulSoup
from selenium.webdriver import Edge
import os,requests,zipfile,platform,base64
_fp=os.path.dirname(os.path.abspath(__file__))
def _getmsedgedriver():
    resp=requests.get("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
    soup=BeautifulSoup(resp.content,"lxml")
    urls=[i["href"] for i in soup.select_one(".driver-download__meta").select("a")]
    pf=platform.architecture()
    if "Windows" in pf[1]:
        if "64" in pf[0]:
            url=urls[1]
        else:
            url=urls[0]
    elif "ELF" in pf[1]:
        url=urls[3]
    else:
        url=urls[2]
    resp=requests.get(url)
    with zipfile.ZipFile(BytesIO(resp.content),"r")as z:
        with open(os.path.join(_fp,"msedgedriver.py"),"wb") as f:
            f.write(z.read("msedgedriver.exe"))
class lazyEdge(Edge):
    def __init__(self,headless=False,**kargs):
        # capabilities={"ms:edgeOptions":{'extensions': [],'args': ['--headless','--disable-gpu',]}} if headless else None
        if headless:
            if "capabilities" in kargs:
                if "ms:edgeOptions" in kargs["capabilities"]:
                    if "args" in kargs["capabilities"]["ms:edgeOptions"]:
                        kargs["capabilities"]["ms:edgeOptions"]["args"]=list(set(kargs["capabilities"]["ms:edgeOptions"]["args"]+['--headless','--disable-gpu',]))
                    else:
                        kargs["capabilities"]["ms:edgeOptions"]["args"]=['--headless','--disable-gpu',]
                    if not "extensions" in kargs["capabilities"]["ms:edgeOptions"]:
                        kargs["capabilities"]["ms:edgeOptions"]["extensions"]=[]
                else:
                    kargs["capabilities"]["ms:edgeOptions"]={'extensions': [],'args': ['--headless','--disable-gpu',]}
            else:
                kargs["capabilities"]={"ms:edgeOptions":{'extensions': [],'args': ['--headless','--disable-gpu',]}}
        try:
            super(lazyEdge,self).__init__(os.path.join(_fp,"msedgedriver.py"),**kargs)
        except:
            _getmsedgedriver()
            super(lazyEdge,self).__init__(os.path.join(_fp,"msedgedriver.py"),**kargs)
    def img2bin(self,imgNode,return_Extension_Name=False):
        s=self.execute_script("""
        var canvas = document.createElement("canvas");  
        var img=arguments[0];
        canvas.width = img.width;  
        canvas.height = img.height;  
        var ctx = canvas.getContext("2d");  
        ctx.drawImage(img, 0, 0, img.width, img.height);  
        var ext = img.src.substring(img.src.lastIndexOf(".")+1).toLowerCase();  
        var dataURL = canvas.toDataURL("image/"+ext);  
        return dataURL;
        """,imgNode)
        if return_Extension_Name:
            return s[s.find("/")+1:s.find(";")],base64.b64decode(s[s.find(",")+1:])
        return base64.b64decode(s[s.find(",")+1:])

    def __del__(self):
        try:
            self.quit()
        except:
            pass
if __name__=="__main__":
    a=lazyEdge()
    a.get("https://www.bilibili.com/")