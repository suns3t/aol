# Atlas of Oregon Lakes

## Install

    virtualenv-2.6 --no-site-packages .env 
    source .env/bin/activate
    pip install -r requirements.txt

If you have trouble installing psycopg2, you may need to add the path to
`pg_config` to your `$PATH`. You can find the proper path by using `locate pg_config`.
On my system, this does the trick:

    export PATH=/usr/pgsql-9.2/bin:$PATH

Pillow is required, (docs here)[https://github.com/python-imaging/Pillow]. You
will probably need to install `libjpeg-devel` and `libtiff-devel`

Create a local copy of the example settings, and configure the SECRET_KEY and DB config:
    
    cp aol/settings/example.py aol/settings/local.py
    vi aol/settings/local.py

Copy all the aol photos to the media dir

    rsync -v USERNAME@circe.rc.pdx.edu:/vol/www/aol/htdocs/lake_photos/* media/photos


