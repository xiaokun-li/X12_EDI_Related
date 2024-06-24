# _*_ coding:utf-8 _*_

class Edi846Generator:
    def __init__(self, sender_id, receiver_id, date, purchase_order_number):
        self.template = self.get_template()
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.date = date
        self.purchase_order_number = purchase_order_number
        self.lines = []

    def get_template(self):
        return """
                  ISA*00*          *00*          *ZZ*{sender_id}*ZZ*{receiver_id}*{date}*0802*U*00401*000000001*0*T*:~
                  GS*PO*{sender_id}*{receiver_id}*{date}*0803*1*X*004010~
                  ST*846*{purchase_order_number}*005010X217~
                  N1*ST*{sender_company}*92*{sender_tax_id}~
                  N1*BT*{receiver_company}*91*{receiver_tax_id}~
                  N1*SH*{shipper_company}*92*{shipper_tax_id}~
                  N1*BN*{beneficiary_name}*92*{beneficiary_tax_id}~
                  PO1*1*EA*{price}*EDI~
                  PID*F****{product_description}~
                  CTT*1~
                  SE*9*{purchase_order_number}~
                  GE*1*1~
                  IEA*1*000000001~
               """

    def add_line_item(self, product_description, price):
        self.lines.append((product_description, price))

    def generate_edi(self):
        edi_content = self.template.format(
            sender_id=self.sender_id,
            receiver_id=self.receiver_id,
            date=self.date,
            purchase_order_number=self.purchase_order_number,
            sender_company="SENDER COMPANY NAME",
            sender_tax_id="987654321",
            receiver_company="RECEIVER COMPANY NAME",
            receiver_tax_id="123456789",
            shipper_company="SHIPPER COMPANY NAME",
            shipper_tax_id="987654321",
            beneficiary_name="BENEFICIARY NAME",
            beneficiary_tax_id="123456789",
            price="19.95",  # 示例价格，实际应从数据库获取
            product_description="PRODUCT DESCRIPTION"  # 示例描述，实际应从数据库获取
        )

        for line in self.lines:
            edi_content += f"PO1*1*EA*{line[1]}*EDI~\n"
            edi_content += f"PID*F****{line[0]}~\n"

        return edi_content

# 使用示例
if __name__ == "__main__":
    generator = Edi846Generator(
        sender_id="SENDERID",
        receiver_id="RECEIVERID",
        date="20061230",
        purchase_order_number="0001"
    )

    # 假设从数据库获取的数据
    generator.add_line_item("Product Description 1", 19.95)
    generator.add_line_item("Product Description 2", 29.95)

    edi_content = generator.generate_edi()
    print(edi_content)