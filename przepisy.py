# coding=utf-8
import webapp2
import logging 
from rendering import BaseHandler
from datetime import datetime
from google.appengine.ext import db
import models
import urllib
from google.appengine.api import images


def RmPolishChars(str):
    str=str.replace(u" ",u"_")
    str=str.replace(u"Ą",u"A")
    str=str.replace(u"ą",u"a")
    str=str.replace(u"Ć",u"C")
    str=str.replace(u"ć",u"c")
    str=str.replace(u"Ę",u"E")
    str=str.replace(u"ę",u"e")
    str=str.replace(u"Ł",u"L")
    str=str.replace(u"ł",u"l")
    str=str.replace(u"Ń",u"N")
    str=str.replace(u"ń",u"n")
    str=str.replace(u"Ó",u"O")
    str=str.replace(u"ó",u"o")
    str=str.replace(u"Ś",u"S")
    str=str.replace(u"ś",u"s")
    str=str.replace(u"Ż",u"Z")
    str=str.replace(u"ż",u"z")
    str=str.replace(u"Ź",u"Z")
    str=str.replace(u"ź",u"z")
    return str

class MainPage(BaseHandler):
    def get(self):
        logging.info("main page")
        self.response.headers['Content-Type']='text/html'
        
        self.render("main.html",dt=datetime.now())
    
        
class Signup(BaseHandler):
    def get(self):
        logging.info("signup")

class Login(BaseHandler):
    def get(self):
        logging.info("login")
        
class Logout(BaseHandler):
    def get(self):
        logging.info("logout")
        
class EditPage(BaseHandler):
    def get(self,article):
        logging.info("edit page")
        title=article[1:]
        content=u""
        skladniki=u""
        a=models.Article.by_key(title)
        if a:
            title=a.title
            content=a.content
            skladniki=a.skladniki
        self.render(u"nowyprzepis.html",title=title, content=content, skladniki=skladniki)
        
            
    def post(self,article):
        img = self.request.get('img')
        title=content=self.request.get("name")
        logging.info(title)
        skladniki=self.request.get("skladniki")
        content=self.request.get("content")
        key = RmPolishChars(title);
        if title and content and skladniki:
            a = models.Article.by_key(key)
            if a: 
                a.delete()
                if img:
                    img_blob = db.Blob(img)
                else:
                    img_blob = None 
                    a=models.Article(parent=models.article_key(),\
                              key_name=key,\
                               image = img_blob,\
                                title=title,\
                                 skladniki=skladniki,\
                                  content=content) 
            else:
                if img:
                    img_blob = db.Blob(img) 
                else: img_blob = None 
                a=models.Article(parent=models.article_key(),\
                                  key_name=key,\
                                   image = img_blob,\
                                    title=title,\
                                     skladniki=skladniki,\
                                      content=content)
            a.put()
            self.redirect("/" + key)
        else:
            error=u"Podaj poprawna zawartosc artykulu!"
            self.render("nowyprzepis.html",content=content, title=article[1:], error=error)


class GetImage(BaseHandler):
    def get(self):
        article = db.get(self.request.get('img_id'))
        if article.image:
            self.response.headers['Content-Type'] = 'image/jpg'
            self.response.out.write(article.image)
        else:
            self.response.out.write('No image')
  
class Przepis(BaseHandler):
    def get(self,article):
        logging.info("wiki page")
        title=article[1:]
        a=models.Article.by_key(title)
        if a:
            logging.info(a.key().name())
            self.render("article-show.html",a=a)
        else:
            self.redirect("/_edit"+article)


class Articles(BaseHandler):
    def get(self):
        articles = models.Article.all()
        if articles:
            self.render("articles.html",articles=articles)
        else:
            self.redirect("/")
    
    def post(self):
        filter = self.request.get("wyszukaj_filtr").split()
        logging.info(filter)
        _articles = models.Article.all()
        if _articles:
            articles = []
            
            for article in _articles:
                t = True
                for skladnik in filter:
                    if article.skladniki.find(skladnik)==-1:
                        t = False
                        break
                if t:
                    articles.append(article)
            
            # wyświetlam przepisy, które przeszły przez filtr
            if articles:
                self.render("articles.html",articles=articles)
            else:
                error=u"Nie znaleziono przepisów"
                self.render("articles.html",articles=articles, error=error)
            
            
class Onas(BaseHandler):
    def get(self):
        self.render("o-nas.html")
        logging.info("Onas")




        
PAGE_RE=r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app=webapp2.WSGIApplication([('/',MainPage),
                             ('/o-nas', Onas),
                             ('/articles', Articles),
                            ('/signup',Signup),
                            ('/login',Login),
                            ('/logout',Logout),
                            ('/_edit'+PAGE_RE,EditPage),
                            ('/img', GetImage),
                            (PAGE_RE,Przepis)],
                            debug=True)
                            
def main():
    logging.info("main()")
    app.run()
    
if __name__=='__main__':
    main()                         