### **🖤 Devils Fire**
☠️ Buy spells, sell curses and find all the ingredients for your next witchery adventure. Devils Fire  the top e-commerce for demons witches and creatures.

👹 In this ebay-like website the users post listings, make bids and interact with others in the comments sections. The owner of the listing decides when to close the bid and the highest bidder gets the price.

🐉 Users can have listings on their watchlist and search listings by category.  Check the bid history on the listing and find out how much money is being offered around!

### **🌸 Django**
This is the fantasy ecommerce I made up for my second project for the **web programming with python and javascript** course from Harvard CS50 courses.

Before taking the class I didnt even know what Django was. But I know understand what a powerfull framework it is!
👩🏻‍💻I learned a lot about backend side programming. And I got to like the way django works, I think is very orgnized and easy to learn.
It took me a while to finish this project and a lot of google searches but I can now say Im happy with how the first version turned out!


### **🖤 Favorite line**
👁️In views.py figuring out how to post comments without the page reloading was a big challenge. And it felt so good once it worked!

🗨️The comments section and the bid history section are the parts Im most proud of

In this line Im rendering an html I made just for the comment section. I then send it thought an HTTP response to be managed by JavaScript on the clients side.
```javascript
context = {'comments': listing.comments.all()}
rendered_comments = render_to_string("auctions/comments.html", context)
return HttpResponse(rendered_comments)
```
