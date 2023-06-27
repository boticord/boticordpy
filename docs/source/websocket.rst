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
.. function:: comment_removed(data)
    
    Called when comment is deleted.