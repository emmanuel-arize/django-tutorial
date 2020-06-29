# setting staic files

```python
# set all these
STATIC_URL = '/static/'
STATICFILES_DIRS=[
os.path.join(BASE_DIR,'static'),]

STATIC_ROOT=os.path.join(os.path.dirname(BASE_DIR),'static_cdn')

# after setting them them type
python manage.py collectstatic

# if you what to create a customize css
1. open the staic directory
2. create a css folder
3. then the name_of_css.css
4. then python manage.py collectstatic again
```