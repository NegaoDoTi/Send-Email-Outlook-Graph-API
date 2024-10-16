from msal import ConfidentialClientApplication
from requests import post
from json import dumps
from config.config import config_env


class SendEmailOutlook():
    def __init__(self) -> None:
        self.__client_secret = config_env["ms_graph"]["client_secret"]
        self.__client_id = config_env["ms_graph"]["client_id"]
        self.__scopes = ["https://graph.microsoft.com/.default"]
        self.__tenant_id = config_env["ms_graph"]["tenant_id"]
        self.__email = config_env["ms_graph"]["email"]
        self.__authority = f"https://login.microsoftonline.com/{self.__tenant_id}"

    def __construct_msal_app(self) -> ConfidentialClientApplication:
        return ConfidentialClientApplication(
            client_id=self.__client_id,
            authority=self.__authority,
            client_credential=self.__client_secret
        )
        
    def get_access_token(self) -> str:
        msal_app = self.__construct_msal_app()
        result = msal_app.acquire_token_for_client(scopes=self.__scopes)
        
        if "access_token" in result:
            return result["access_token"]
        else:
            raise Exception(f"Erro ao obter o token de acesso: {result.get('error_description')}")
        
    def send_email(self, text:str, email:str, access_token:str ) -> str:
        graph_endpoint = f"https://graph.microsoft.com/v1.0/users/{self.__email}/sendMail"
        email_data = {
            "message" : {
                "subject" : "Este é um email de teste",
                "body" : {
                    "contentType" : "Text",
                    "content" : f"{text}"
                },
                "toRecipients" : [
                    {
                        "emailAddress" : {
                            "address" : "viniciusluciano2012@hotmail.com"
                        }
                    }
                ]
            },
            "saveToSentItems": "true"
        }
        
        headers = {
            "Authorization" : f'Bearer {access_token}',
            "Content-Type" : "application/json"
        }
        
        response = post(graph_endpoint, headers=headers, data=dumps(email_data))
        
        if response.status_code == 202:
            return "Sucesso ao enviar email!"
        else:
            return f"Falha ao enviar email {response.text}"
        
    
if __name__ == "__main__":
    
    try:
        send_email = SendEmailOutlook()
        token = send_email.get_access_token()
        result = send_email.send_email("Test", "test@test.com.br", token)
        
        print(result)
    except Exception as e:
        print(e)

