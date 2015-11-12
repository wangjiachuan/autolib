from nameko.events import EventDispatcher, event_handler
from mandrill_send_email import *

class MailService(object):
    name = 'mails'
    
    def __init__(self):
        self.to=' '
        self.subject ='pay mail confirmation'
        self.msg =' '
        self.senderMandrill = sendEmail_Mandrill()

    @event_handler('payments', 'payment_received')
    def handle_an_event(self, payload):
        """
        sends the email using data extracted from payload
        :param payload: validated data
        """
        
	# extract the email element from payload
	self.to=payload['client'][email]
        self.msg =""""
		    Dear {payee},
	            You have received a payment of {amout} {currency} from {client} {email}
		    yours
		    student
		""".format(payee=payload[][],amout=payload['payment'][amount],currency=payload['payment'][amount],client=payload['payment'][amount],email=payload['payment'][amount]) 
		
	# send the email out
	try:
		self.senderMandrill.send(self.subject,self.to, self.msg)
        except:
        	pass
s
			
			
if __name__ == '__main__':
    
