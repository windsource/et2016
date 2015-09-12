# README #

This source code contains the registration process for [KLM Europatreffen 2016](http://www.europatreffen2016.eu). It contains an application for [web2py](http://www.web2py.com/).

After installation it provides two URIs, one for users to register the other for administrators.

```
/et2016/default/create
/et2016/orga/list
```

### How do I get set up? ###

* Install [web2py](http://www.web2py.com/)
* copy the `et2016` folder in `applications` directory
* copy `et2016/models/0_login_example.py`to `et2016/models/0_login.py` and enter your db (sqlite or mysql), the credentials for the db and the credentials for your email provider.

### How do test it?

See [tests](tests/README.md) section


That's it.

Have fun.

windsource@gmx.de
