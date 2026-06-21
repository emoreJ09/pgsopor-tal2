import streamlit as st
import db  
import os  
from datetime import datetime  
from io import BytesIO

def generate_excel_bytes(project_name, location, pow_items):
    """
    Ito ang lohika na gumagawa at nag-o-automate ng totoong Microsoft Excel file
    gamit ang openpyxl, ngunit ibinabalik ito bilang 'Bytes' para ma-download sa Web.
    """
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Program of Work"
    ws.views.sheetView[0].showGridLines = True

    # 📑 PRINT & PAGE SETUP FOR LEGAL SIZE
    ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
    ws.page_setup.paperSize = ws.PAPERSIZE_LEGAL
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1   
    ws.page_setup.fitToHeight = 0  

    ws.page_margins.left = 0.5
    ws.page_margins.right = 0.5
    ws.page_margins.top = 0.75
    ws.page_margins.bottom = 0.75

    font_title = Font(name="Arial", size=10, bold=True)
    font_regular = Font(name="Arial", size=10)
    font_bold_body = Font(name="Arial", size=10, bold=True)
    
    align_center = Alignment(horizontal="center", vertical="center")
    align_left = Alignment(horizontal="left", vertical="center")
    align_right = Alignment(horizontal="right", vertical="center")

    ws['A1'] = "Republic of the Philippines"
    ws['A2'] = "PROVINCE   OF   NUEVA   ECIJA"
    ws['A3'] = "Palayan City"
    ws['A4'] = "PROVINCIAL GENERAL SERVICES OFFICE"
    ws['A6'] = "PROGRAM OF WORKS"
    
    for r in range(1, 7):
        if ws.cell(row=r, column=1).value:
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
            header_cell = ws.cell(row=r, column=1)
            header_cell.alignment = align_center
            header_cell.font = font_title

    ws['A7'] = f"Project: {project_name}"
    ws['A8'] = f"Location: {location}"
    ws['A7'].font = font_bold_body
    ws['A8'].font = font_bold_body

    headers_list = ["ITEM", "QTY", "UNIT", "DESCRIPTION", "UNIT PRICE", "AMOUNT"]
    for col_num, header_text in enumerate(headers_list, start=1):
        c_cell = ws.cell(row=9, column=col_num, value=header_text)
        c_cell.font = font_bold_body
        c_cell.alignment = align_center
        
    row_tracker = 10
    computed_total = 0.0
    
    for idx, item in enumerate(pow_items, start=1):
        qty = float(item[0]) 
        unit = item[1]
        raw_name = item[2]
        raw_price = item[3]
        
        name = str(raw_name).replace("\n", " ").replace("\r", " ").strip()
        try:
            price = float(raw_price) if raw_price is not None else 0.0
        except ValueError:
            price = 0.0

        amount = qty * price
        computed_total += amount

        ws.cell(row=row_tracker, column=1, value=idx).alignment = align_center
        ws.cell(row=row_tracker, column=2, value=qty).alignment = align_center
        ws.cell(row=row_tracker, column=3, value=unit).alignment = align_center
        ws.cell(row=row_tracker, column=4, value=name).alignment = align_left
        
        p_cell = ws.cell(row=row_tracker, column=5, value=price)
        p_cell.number_format = '#,##0.00'
        p_cell.alignment = align_right
        
        a_cell = ws.cell(row=row_tracker, column=6, value=amount)
        a_cell.number_format = '#,##0.00'
        a_cell.alignment = align_right

        for column_pos in range(1, 7):
            ws.cell(row=row_tracker, column=column_pos).font = font_regular
            
        row_tracker += 1

    row_tracker += 1 
    ws.cell(row=row_tracker, column=5, value="Total  P").font = font_bold_body
    ws.cell(row=row_tracker, column=5).alignment = Alignment(horizontal="right", vertical="center")
    
    f_total_cell = ws.cell(row=row_tracker, column=6, value=computed_total)
    f_total_cell.font = font_bold_body
    f_total_cell.number_format = '"P" #,##0.00'
    f_total_cell.alignment = align_right

    double_bottom_border = Border(bottom=Side(style='double'))
    last_item_amount_cell = ws.cell(row=row_tracker - 2, column=6)
    last_item_amount_cell.border = double_bottom_border

    row_tracker += 2
    ws.cell(row=row_tracker, column=1, value="Prepared by:                                                                                Checked by:").font = font_regular
    
    row_tracker += 2
    ws.cell(row=row_tracker, column=1, value="        JONATHAN G. LADIGNON                                                                BENJAMIN N. RAMOS JR.").font = font_bold_body
    
    row_tracker += 1
    ws.cell(row=row_tracker, column=1, value="             Admin. Officer III                                                                 Engineer II").font = font_regular

    row_tracker += 2
    ws.cell(row=row_tracker, column=1, value="Noted by:                                                                                      Recommending Approval:").font = font_regular

    row_tracker += 2
    ws.cell(row=row_tracker, column=1, value="        MARIO T. MARIANO                                                                     ENGR. FLORECIO M. VALINO").font = font_bold_body
    
    row_tracker += 1
    ws.cell(row=row_tracker, column=1, value="             Engineer IV                                                                          PGS-Officer").font = font_regular

    row_tracker += 2
    ws.cell(row=row_tracker, column=4, value="                                     Approved:").font = font_regular

    row_tracker += 2
    ws.cell(row=row_tracker, column=4, value="                     HON. AURELIO M. UMALI").font = font_bold_body
    row_tracker += 1
    ws.cell(row=row_tracker, column=4, value="                                           Governor").font = font_regular

    column_widths = {'A': 4.57, 'B': 4.86, 'C': 7.00, 'D': 47.14, 'E': 11.57, 'F': 14.57}
    for col_letter, width_size in column_widths.items():
        ws.column_dimensions[col_letter].width = width_size

    ws.row_dimensions[9].height = 20
    for r_idx in range(10, row_tracker + 15):
        ws.row_dimensions[r_idx].height = 16

    if len(pow_items) > 35:
        from openpyxl.worksheet.pagebreak import Break
        ws.row_breaks.append(Break(id=45))

    excel_stream = BytesIO()
    wb.save(excel_stream)
    excel_stream.seek(0)
    return excel_stream.getvalue()


def show_excel_preview_streamlit(pow_id):
    """
    Ito ang main function para sa Streamlit UI.
    Ipinapakita nito ang text preview at nagbibigay ng Download Button.
    """
    proj_info = db.get_project_details(pow_id)
    pow_items = db.get_items_by_project(pow_id)

    if not proj_info:
        st.error("❌ Hindi mahanap ang detalye ng proyektong ito sa database.")
        return

    project_name, location = proj_info[0], proj_info[1]

    # --- RENDER TEXT PREVIEW SA WEB ---
    st.subheader("📄 Print Layout Preview")
    
    preview_output = f"""
                         Republic of the Philippines
                       PROVINCE   OF   NUEVA   ECIJA
                                Palayan City
                     PROVINCIAL GENERAL SERVICES OFFICE
                     
                              PROGRAM OF WORKS
                              
    Project:  {project_name}
    Location: {location}
    {"=" * 80}
    {"ITEM":<6}{"QTY":<8}{"UNIT":<8}{"DESCRIPTION":<35}{"UNIT PRICE":<12}{"AMOUNT":<11}
    {"=" * 80}"""
    
    grand_total = 0.0
    for idx, item in enumerate(pow_items, start=1):
        qty = float(item[0])
        unit = item[1]
        name = str(item[2]).replace("\n", " ").strip()
        price = float(item[3]) if item[3] is not None else 0.0
        amount = qty * price
        grand_total += amount
        
        short_name = name[:32] + "..." if len(name) > 32 else name
        preview_output += f"\n{idx:<6}{qty:<8.2f}{unit:<8}{short_name:<35}{price:>12,.2f}{amount:>11,.2f}"

    preview_output += f"\n{'-' * 80}\n{'TOTAL':<57}P {grand_total:>20,.2f}\n{'=' * 80}\n"
    preview_output += f"\nPrepared by: Jonathan G. Ladignon    Checked by: Benjamin N. Ramos Jr"
    
    st.code(preview_output, language="text")

    # --- UTILITY EXCEL DOWNLOAD TRIGGER ---
    st.markdown("---")
    st.subheader("📥 Actions")
    
    try:
        excel_data = generate_excel_bytes(project_name, location, pow_items)
        clean_project_name = project_name.replace(' ', '_').replace('/', '-').replace('\\', '-')
        filename = f"POW_{clean_project_name}.xlsx"

        st.download_button(
            label="📥 DOWNLOAD OFFICIAL EXCEL FILE",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"May error sa pagbuo ng Excel download link: {e}")
