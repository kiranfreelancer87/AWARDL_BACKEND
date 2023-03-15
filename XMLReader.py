import xml.etree.ElementTree as ET

tree = ET.parse('causelist.xml')
root = tree.getroot()

arrHeaders = []
for header in root[0]:
    arrHeaders.append(header.attrib.get('name'))

print(arrHeaders)
print(len(arrHeaders))
srno = ''
arrColumns = ['sr_no', 'cino', 'case_no', 'next_date', 'court_no', 'ctype', 'originalsr_no', 'case_remark',
              'causelist_type', 'causelist_period', 'list_from_date', 'list_to_date', 'causelist_date', 'for_bench_id',
              'purpose_cd', 'reg_dt', 'filing_dt', 'section_id', 'on_filing', 'clink_code', 'civilt_court_no',
              'civilt_date_next_list', 'civilt_purpose_next', 'civilt_sr_no', 'civilt_causelist_type', 'elimination',
              'causelist_sr_no', 'cause_list_eliminate', 'ia_no', 'ia_next_date', 'ia_flag', 'unique_no', 'search_case',
              'initial_status', 'final_status', 'cause_case_type', 'cause_reg_no', 'cause_reg_year', 'takenonboard',
              'oldbenchid', 'newbenchid', 'olink_code', 'ia_case_type', 'hashkey', 'bunch_code', 'purpose_priority',
              'short_order', 'prev_short_order', 'amd', 'create_modify']

print(arrColumns)

print(len(arrHeaders), len(arrColumns))

diffColumns = []

for column in arrColumns:
    if column not in arrHeaders:
        diffColumns.append(column)
    else:
        print(column)

print(diffColumns)
print(len(diffColumns))
exit()
for row in root[1]:
    for column in row:
        print(column.attrib.get("name") + "(" + column.text + ")")

for root_child in root:
    print(root_child)
    for root_child_child in root_child:
        print("\t", root_child_child)
        for root_child_child_child in root_child_child:
            print("\t\t", root_child_child_child)
            print("\t\t", root_child_child_child.text)
