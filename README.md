domain_manager
==============

Just one step to auto-update domain's DNS record @name.com where you do not have static public IP address.


##Configure your account information first

You should open the file config.yml, and edit it with your account information and domains need to update.

* Just like this:

account:
   user_name: hagerhu
   api_token: 9a872318asca1b3b2c234d1b1d773ed4385e3ab

domains_update:
    - hagerhu.com
	- cmcn.me


##Run the install script in the current directory

cd $PATH_DOMAIN_MANAGER
sh ./install.sh

So enjoy it!

This will create a cronjob for you to get your public IP address periodically(5 mins) and use API service of @name.com to update configure'd domain's DNS A record.