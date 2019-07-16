Running your own instance
=========================

API Keys and tokens
-------------------

The bot requires some API keys in order to work properly. Make sure not
to share any of these keys with anyone, think of them as passwords.

+---------------------------+-------------------+-----------+-----------+
| Service                   | Where             | How       | Why       |
+===========================+===================+===========+===========+
| Discord bot token         | `Discord          | If you    | This is   |
|                           | Developer         | don’t     | required  |
|                           | Portal`_          | have an   | to login  |
|                           |                   | applicati | to your   |
|                           |                   | on        | bot’s     |
|                           |                   | for your  | user      |
|                           |                   | bot       | profile.  |
|                           |                   | already,  |           |
|                           |                   | `create   |           |
|                           |                   | one`_ in  |           |
|                           |                   | the       |           |
|                           |                   | developer |           |
|                           |                   | portal.   |           |
|                           |                   | Head to   |           |
|                           |                   | ``General |           |
|                           |                   |  Informat |           |
|                           |                   | ion``     |           |
|                           |                   | in your   |           |
|                           |                   | bot’s     |           |
|                           |                   | user      |           |
|                           |                   | page,     |           |
|                           |                   | click     |           |
|                           |                   | ``Click t |           |
|                           |                   | o reveal` |           |
|                           |                   | `         |           |
|                           |                   | (under    |           |
|                           |                   | ``CLIENT  |           |
|                           |                   | SECRET``) |           |
+---------------------------+-------------------+-----------+-----------+
| Wolfram Alpha API         | `Wolfram|Alpha    | Click     | Used with |
|                           | APIs`_            | ``Get API | the       |
|                           |                   |  Access`` | ``query`` |
|                           |                   | under     | command.  |
|                           |                   | ``Get Sta |           |
|                           |                   | rted for  |           |
|                           |                   | Free``    |           |
|                           |                   | and fill  |           |
|                           |                   | in the    |           |
|                           |                   | required  |           |
|                           |                   | informati |           |
|                           |                   | on.       |           |
+---------------------------+-------------------+-----------+-----------+
| osu! API                  | `Request API      | Refer to  | Used with |
|                           | access`_          | the `osu! | commands  |
|                           |                   | api       | in the    |
|                           |                   | wiki`_.   | osu! cog. |
+---------------------------+-------------------+-----------+-----------+
| Omdb API                  | `Generate API     | Select    | Used with |
|                           | key`_             | ``FREE! ( | the       |
|                           |                   | 1,000 dai | ``imdb``  |
|                           |                   | ly limit) | command.  |
|                           |                   | ``        |           |
|                           |                   | and enter |           |
|                           |                   | a valid   |           |
|                           |                   | email     |           |
|                           |                   | address   |           |
|                           |                   | (temporar |           |
|                           |                   | y         |           |
|                           |                   | emails    |           |
|                           |                   | are       |           |
|                           |                   | purged.)  |           |
+---------------------------+-------------------+-----------+-----------+
| LastFM API                | `Create API       | Enter the | Used with |
|                           | account`_         | necessary | the       |
|                           |                   | informati | ``lastfm` |
|                           |                   | on.       | `         |
|                           |                   | Callback  | command.  |
|                           |                   | URL is    |           |
|                           |                   | not       |           |
|                           |                   | required. |           |
+---------------------------+-------------------+-----------+-----------+

Saving your tokens for use with the bot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copy the `template-secrets.json`_ from the main repository and name it
``secrets.json``. Put it in the same directory as
``template-secrets.json`` (``rufus/src/secrets.json``). Fill in the keys
with the appropriate values.

.. code:: json

   {
       "botToken": "s3cr47-b07-70k3n",
       "wolfram": "w01fr4m-k3y",
       "osu": "p3r-4-m4nc3-p01n75",
       "omdb": "m0v135-4nd-53r135",
       "lastfm": "11573n-2-mu51c"
   }

Setting up your environment
---------------------------

Clone the repository -
``git clone -b master https://github.com/runarsf/rufus.git``

With docker
~~~~~~~~~~~

Prerequisites
'''''''''''''

::

   git
   docker
   docker-compose

``WARNING`` Do not run docker as root!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This can cause docker to change the ownerships of some files to root. If
you’re having troubles with docker or docker-compose, run this to add
yourself to the docker group. The command will take effect on next
login, and will be effective in your current shell session.

.. code:: bash

   newgrp docker
   systemctl start docker

Starting the bot
^^^^^^^^^^^^^^^^

.. code:: bash

   docker-compose up -d
   docker-compose logs -f

Rebuilding
^^^^^^^^^^

.. code:: bash

   docker-compose build

Stopping
^^^^^^^^

.. code:: bash

   docker-compose down

Without docker
~~~~~~~~~~~~~~

.. _prerequisites-1:

Prerequisites
^^^^^^^^^^^^^

::

   git
   python>=3.6
   pip>=9.0.1
   docker
   docker-compose

-  As well as all of the Python packages in `requirements.txt`_.

   -  Can be easily installed with
      ``python3 -m pip install -r ./requirements.txt``

-  Docker is still needed in use with the runner command.

Detaching from the process but still leaving it running
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

I suggest using tmux, these commands should be able to get you started.
You can detach from a session using :kbd:`CTRL+b` :kbd:`d` to quit.

::

   # Create a new session.
   tmux new -s rufus
   # Attach to existing session
   tmux a -t rufus

.. _Discord Developer Portal: https://discordapp.com/developers/applications/
.. _create one: https://discordjs.guide/preparations/setting-up-a-bot-application.html
.. _Wolfram|Alpha APIs: https://products.wolframalpha.com/api/
.. _Request API access: https://osu.ppy.sh/p/api
.. _osu! api wiki: https://github.com/ppy/osu-api/wiki
.. _Generate API key: https://www.omdbapi.com/apikey.aspx
.. _Create API account: https://www.last.fm/api/account/create
.. _template-secrets.json: https://github.com/runarsf/rufus/blob/master/src/template-secrets.json
.. _requirements.txt: https://github.com/runarsf/rufus/blob/master/src/requirements.txt
