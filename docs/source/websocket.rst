.. currentmodule:: boticordpy.websocket

###########
WebSocket
###########

BotiCord Websocket
-------------------

.. autoclass:: BotiCordWebsocket
    :exclude-members: listener
    :inherited-members:

    .. automethod:: BotiCordWebsocket.listener()
        :decorator:


Notification types
-------------------
.. function:: up_added(data)

    Called when up is added.

.. function:: comment_added(data)

    Called when comment is added.

.. function:: comment_edited(data)

    Called when comment is deleted.
    
.. function:: comment_removed(data)

    Called when comment is deleted.

