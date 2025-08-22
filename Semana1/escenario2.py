# # ANTES (OCP)
# class PaymentProcessor:
#     def process(self, payment_type: str, amount: float):
#         if payment_type == "cash":
#             print(f"Efectivo: {amount}")
#         elif payment_type == "card":
#             print(f"Tarjeta: {amount}")
#         elif payment_type == "transfer":
#             print(f"Transferencia: {amount}")
#         else:
#             raise ValueError("Tipo no soportado")

# if __name__ == "__main__":
#     PaymentProcessor().process("card", 100.0)


# ANTES (OCP)

from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CashPayment(Payment):
    def pay(self, amount: float):
        print(f"Efectivo: {amount}")

class CardPayment(Payment):
    def pay(self, amount: float):
        print(f"Tarjeta: {amount}")

class TransferPayment(Payment):
    def pay(self, amount: float):
        print(f"Transferencia: {amount}")

class PaymentProcessor:
    def __init__(self, payment: Payment):
        self.payment = payment

    def process(self, amount: float):
        self.payment.pay(amount)

if __name__ == "__main__":
    processor = PaymentProcessor(CardPayment())
    processor.process(100.0)