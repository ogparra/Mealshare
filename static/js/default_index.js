// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    self.print_bool = function(){
    };

    self.add_item = function () {
        $.post(add_item_url,
            {
                item_content: self.vue.form_item_content,
            },
            function (data) {
                $.web2py.enableElement($("#add_item_submit"));
                self.vue.items.unshift(data.item);
            });
    };

    // method to remove pantry item
    self.remove_item = function(item_id){
        $.item(del_item_url),
           {
               item_id: item_id
           },
           function () {
              var idx = null;
              for(var i = 0; i < self.vue.items.length; i++){
                if(self.vue.items[i].id === item_id) {
                    idx = i + 1;
                     break;
                }
              }
           }
    };
    
    // method to edit pantry item
    self.edit_item = function(){
         $.item(edit_item_url,
            {
                content: self.vue.form_update_content,
                updated_on: self.vue.form_updated_on,
                item_id: self.vue.edit_id
            },
            function () {
                self.get_items()
            });

        self.vue.editing = false;
        self.vue.form_update_content = "";
    };
    
    // method to update quantity
    self.inc_item_quantity = function(item_idx, qty){
         // Inc and dec to desired quantity.
        var i = self.vue.items[item_idx];
        i.item_quantity = Math.max(0, i.item_quantity + qty);
        i.item_quantity = Math.min(i.item, i.item_quantity);
    };
    
    // method to change expiration date
    self.change_expiration = function(){
    
    };
    

    function items_url(start_idx, end_idx) {
        var pp = {
            start_idx: start_idx,
            end_idx: end_idx
        };
        return get_items_url + '?' + $.param(pp);
    }

    self.get_items = function () {
        var num_posts = self.vue.items.length;
        $.getJSON(items_url(0, 4), function (data) {
            self.vue.items = data.items;
            self.vue.has_more = data.has_more;
            self.vue.logged_in = data.logged_in;
        })
    };


    self.add_item = function (){
        self.vue.adding_item = !self.vue.adding_item;
    };

    self.adding_users = function(){
        self.vue.adding_user = !self.vue.adding_user;
    };

    //Function for item quantity
    self.item_quantity = function(x){
        num = self.vue.num_items;
        if(x == 1){
            num++;
        }else{
            if(num != 1){
                num--;
            }
        }
        self.vue.num_items = num;
    };


    self.add_to_pantry = function(){
       console.log(self.vue.item_name+"\n");
       console.log(self.vue.item_exp+"\n");
       console.log(self.vue.num_items+"\n");
        $.post(add_grocery_url,
        {
            item_name: self.vue.item_name,
            exp_date: self.vue.item_exp, 
            num_items: self.vue.num_items,
        },function (data) {
            //$.web2py.enableElement($("#add_post_submit"));
            self.vue.items.unshift(data.item);
        });
    }

    self.edit_item = function(item_id, items){
        //self.vue.editing_item = !self.vue.editing_item;

        for (var i = 0; i < self.vue.items.length; i++) {
            if (self.vue.items[i].id === item_id) {
                // If I set this to i, it won't work, as the if below will
                // return false for items in first position.
                //idx = i + 1;
                self.vue.item_iden = self.vue.items[i].id; 

                self.vue.item_edit_name = self.vue.items[i].item_name;
                self.vue.item_edit_exp = self.vue.items[i].exp_date;
                self.vue.item_edit_num = self.vue.items[i].item_num;
                //console.log(item_iden);
                //if the items index matches the item_id, then let me edit the post 
                break;
            }
        }
    }

    self.edit_item_finish = function(item_id, items){
        console.log("inside");


        //update won't happen automatically
        for (var i = 0; i < self.vue.items.length; i++) {
            if (self.vue.items[i].id === item_id) {
                var num = i;
                break;
            }
        }
        
         $.post(edit_grocery_url, 
            {
                item_id: item_id,
                item_name: self.vue.item_edit_name,
                exp_date: self.vue.item_edit_exp,
                item_num: self.vue.item_edit_num,
            },function (data) {
                console.log(data.edit_item.item_name);
                self.vue.items[num].item_name = data.edit_item.item_name;
                self.vue.items[num].exp_date = data.edit_item.exp_date;
                self.vue.items[num].item_num = data.edit_item.item_num;

            });
        
        self.get_items();
        self.vue.item_iden = -1;
    }

    self.delete_item = function(item_id, items) {
        console.log(item_id);
        $.post(del_grocery_url,
            {
                item_id: item_id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.items.length; i++) {
                    if (self.vue.items[i].id === item_id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.items.splice(idx - 1, 1);
                }
            }
        )
    };


    /*******************************************************
     *******************************************************
     *******************************************************/

    self.get_users = function () {
        $.getJSON(get_users_url, function(data){
            self.vue.registered_users = data.reg_users;
            self.vue.user_logged_in = data.user;
            self.vue.user_in = data.user_n;
        })
    };

    self.get_profile = function(item_id){
        self.vue.showing_profile = !self.vue.showing_profile;
        $.getJSON(get_profile_url,
            {
                id: item_id            
            }, function (data){
            self.vue.user_profile = data.user;
      });
    }

    self.get_user_list = function(){
        console.log("Got the user list");
        self.vue.clicked_user = !self.clicked_user;
        //if user was clicked change the color of the button to show user is selected
    };

    function user_items_url(useremail){
        var email = { useremail: useremail};
        return get_users_items_url + '?' + $.param(email);
    }

    self.get_users_items = function(email){
        self.vue.f_email_chkmeal = email;
        $.getJSON(user_items_url(email), function(data){
            self.vue.user_items = data.user_items;
        })
        self.get_user_list();
    };

    self.get_logged = function(){
        $.getJSON(logged_in_url, function(data){
            self.vue.logged_in_user = data.logged_in;
        })
    };

    self.add_to_meal = function(item){
        self.vue.meal_num++;
        self.vue.meal_items.push(item);
    };


    self.checkout_meal = function(){

        //Setting date 
        var time = new Date();
        var day_week = time.getDate();
        var mon = time.getMonth() + 1;
        var year = time.getFullYear();
        var hours = time.getHours();
        var mins = time.getMinutes();
        if(mins < 10)
            mins = "0"+mins.toString(); 
        //alert(day_week + "/" + mon +"/" + year +" "+ hours+":"+mins);
        self.vue.set_date = (mon.toString() + "-" + day_week.toString() + "-" +year.toString() +" "+hours.toString() +":"+ mins);
        //alert(time.getDate());

        self.vue.flag = 0;
        for( var i = 0; i < self.vue.meal_items.length; i++){
            post_meal(self.vue.meal_items[i]);
        }
    }

    function post_meal(item){
        if( self.vue.flag === 0){
            self.vue.flag++;
            self.vue.ident_int = Math.random();
            $.post(create_meal_url,{
                item_fuser: self.vue.f_email_chkmeal, 
                item_name : item.item_name,
                item_quan: item.item_num,
                item_exp: item.exp_date,
                item_date: self.vue.set_date,
                item_ident: self.vue.ident_int,
                item_owner: item.email

            }, function (data){
            });

        }else{
            //while(self.vue.first_run != 1){console.log("inside while");}
            $.post(create_meal_url,{
                item_fuser: self.vue.f_email_chkmeal, 
                item_name : item.item_name,
                item_quan: item.item_num,
                item_exp: item.exp_date,
                item_ident: self.vue.ident_int,
                item_date: self.vue.set_date,
                item_owner: item.email

            }, function (data) {
            });
        }    
    }

    self.getting_meals = function () {
        self.vue.is_getting_meals = !self.vue.is_getting_meals;
    };

    self.get_meals = function(){
        $.getJSON(get_meals_url, function (data) {
            self.vue.meals_arr = [[]];
            self.vue.meals_are_empty = false;
            self.vue.meal_reqs = data.meals;
            temp_meal_arr = [];
            var j =0;
            self.vue.meals_arr = [];
            for(var i = 0; i<self.vue.meal_reqs.length; i++){
                item = self.vue.meal_reqs[i];
                if(temp_meal_arr.length == 0){
                    temp_meal_arr.push(item);
                    j++;
                    continue;
                }
                if(temp_meal_arr[j-1].identifier == item.identifier){
                    temp_meal_arr.push(item);
                    j++;
                }else{
                    self.vue.meals_arr.push(temp_meal_arr);
                    temp_meal_arr = [];
                    temp_meal_arr.push(item);
                    j=1;
                }
            }
            self.vue.meals_arr.push(temp_meal_arr);
            /*Testing
            for (var i = 0; i<self.vue.meals_arr.length; i++){
                for (var k = 0; k<self.vue.meals_arr[i].length; k++){
                    alert(self.vue.meals_arr[i][k].item_name);
                    alert(self.vue.meals_arr[i][k].identifier);
                    alert(self.vue.meals_arr[i][k].item_owner);
                    alert(self.vue.meals_arr[i][k].item_exp);
                }
            }*/
        });
    };


    /******************************************************************
     ******************************************************************
     ******************************************************************/

    function add_friend_url(useremail){
        var email = { useremail: useremail};
        return add_friends_url + '?' + $.param(email);
    }

    self.add_friend = function(email){
        console.log("add");
        $.post(add_friend_url(email), function (data) {

            self.vue.get_friends();
        });
    };

    self.get_friends = function(){
        $.getJSON(get_friends_url, function (data) {
            self.vue.friends = data.friends;
            self.vue.requests = data.request;
        })
    };

    function confirm_friend_url(useremail, id){
        var email = {
            useremail: useremail,
            id : id
        };
        return confirm_request_url + '?' + $.param(email);
    }
    self.confirm_request = function(email, id){
        $.post(confirm_friend_url(email, id), function (data) {
            self.vue.get_friends();
        })
    }

    self.delete_user = function(id){
       // alert(id);
        $.post(del_friend_url,
            {
                friend_id: id
            },
            function () {
                var idx = null;
                for (var i = 0; i < self.vue.friends.length; i++) {
                    if (self.vue.friends[i].id === id) {
                        // If I set this to i, it won't work, as the if below will
                        // return false for items in first position.
                        idx = i + 1;
                        break;
                    }
                }
                if (idx) {
                    self.vue.friends.splice(idx - 1, 1);
                }
            }
        )
    };

    self.check_users = function (email){
       //console.log(JSON.parse(check_users_func(email)));
        var value = true;
        for (var i = 0; i < self.vue.friends.length; i++) {
            if (self.vue.friends[i].user_email == email) {
                value = false;
                break;
            }else if(self.vue.friends[i].friend_email == email){
                value = false;
                break;
            }
        }
       //console.log(value);
       return value;
    }


    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            items: [],
            registered_users: [],
            user_items: [],
            unconfirmed: [],
            friends: [],
            requests: [],
            meal_items: [],
            meal_reqs:[],
            meals_arr :[[]],
            adding_item: false,
            bool: false,
            add_item: false,
            add_grocery: null,
            adding_user: false,
            logged_in: false,
            item_name: "",
            item_exp: "",
            item_num: 1,
            item_pantry: null,
            num_items: 1,
            item_edit_name: null,
            item_edit_exp: null,
            item_edit_num: null,
            clicked_user: false,
            user_logged_in: null,
            logged_in_user: null,
            user_in: null,
            meal_num: 0,
            meal_cart: null,
            showing_profile: false,
            user_profile: 0,
            flag: 0,
            f_email_chkmeal: null,
            item_iden: null,
            set_date: "",
            first_run: 0,
            ident_int: null,
            is_getting_meals: false,
            meals_are_empty:true
        },
        methods: {
            //set_name: self.set_name,
            print_bool: self.print_bool,
            remove_item: self.remove_item,
            edit_item: self.edit_item,
            inc_item_quantity: self.inc_item_quantity,
            change_expiration: self.change_expiration,
            print_bool: self.print_bool,
            add_item: self.add_item,
            item_quantity: self.item_quantity,
            add_to_pantry: self.add_to_pantry,
            get_items: self.get_items,
            delete_item: self.delete_item,
            edit_item: self.edit_item,
            edit_item_finish: self.edit_item_finish,
            get_users: self.get_users,
            get_user_list: self.get_user_list,
            get_users_items: self.get_users_items,
            get_logged: self.get_logged,
            adding_users: self.adding_users,
            add_friend: self.add_friend,
            get_friends: self.get_friends,
            confirm_request: self.confirm_request,
            delete_user: self.delete_user, 
            add_to_meal: self.add_to_meal, 
            checkout_meal: self.checkout_meal, 
            check_users: self.check_users,
            get_profile: self.get_profile ,
            getting_meals: self.getting_meals,
        }
    });

    self.get_users();
    self.get_items();
    self.get_logged();
    self.get_friends();
    self.get_meals();
    $("#vue-div").show();

    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
