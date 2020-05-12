class SaleaeGeneratorTrait:
    def get_bindings_name(self):
        return 'saleae'

    def get_bindings_display_name(self):
        return 'Saleae'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().under
