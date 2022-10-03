# ReadME for RPA

## First Steps

Clone repo

Create and activate Virtual Env of your choosing

```
pip intstall -r requirements.txt

```

Open code in editor of choice

Add WordPress username to relevant field (look for the comment)

Add path of Chrome/Chromium executable to relevant field (look for the comment)

## Running File

In active env, run

```
  python main.py
```

You will be prompted to enter your WordPress password

## Other Notes

Pyppeteer comes with an old version of chromium, so it is important to install the latest version of chromium if you don't have it, or just use your existing version of chrom.

As noted above, add the executable path to the relevant variable
