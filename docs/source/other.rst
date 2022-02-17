.. currentmodule:: boticordpy

.. other:

Other Information
=================

##########
Listeners
##########

List of listeners for webhooks

+------------------------+----------------------------------+
|    Boticord Events     |              Meaning             |
+========================+==================================+
|    new_bot_comment     |      On new bot comment          |
+------------------------+----------------------------------+
|    edit_bot_comment    |     On bot comment edit          |
+------------------------+----------------------------------+
|   delete_bot_comment   |     On bot comment delete        |
+------------------------+----------------------------------+
|      new_bot_bump      |       On new bot bump            |
+------------------------+----------------------------------+
|   new_server_comment   |      On new server comment       |
+------------------------+----------------------------------+
|   edit_server_comment  |      On server comment edit      |
+------------------------+----------------------------------+
|  delete_server_comment |      On server comment delete    |
+------------------------+----------------------------------+


##################
Callback functions
##################

.. warning::

    Callback functions must be a **coroutine**. If they aren't, then you might get unexpected
    errors. In order to turn a function into a coroutine they must be ``async def``
    functions.
