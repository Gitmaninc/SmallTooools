import os
import zipfile

def un_zip(src, dst):
    """ src : aa/asdf.zip
        dst : unzip/aa/asdf.zip
    """
    try:
        zip_file = zipfile.ZipFile(src)
        if not os.path.exists(dst):
            os.makedirs(dst)
        for name in zip_file.namelist():
            zip_file.extract(name, dst)
        zip_file.close()
    except zipfile.BadZipfile:
        pass
    except RuntimeError:
        return "pass required"
    except Exception as e: 
        raise


un_zip("./aaa.zip","./unzip/")