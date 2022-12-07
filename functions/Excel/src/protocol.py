import xlsxwriter
from .utils import *


def build_protocol(filename, sorted_data, judge_name, secretary_name):
    # xlsx config
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    worksheet.set_landscape()
    worksheet.center_horizontally()
    worksheet.set_paper(9)

    # styles
    default_style = workbook.add_format({
        'align': 'center',
        'valign': 'vcenter',
        'border': 1,
    })

    green_style = workbook.add_format({
        'bold': True,
        'bg_color': '#ccffcc',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    orange_style = workbook.add_format({
        'bold': True,
        'bg_color': '#ffff99',
        'align': 'center',
        'valign': 'vcenter',
        'border': 1
    })

    # write data
    row_max = len(sorted_data)
    col_max = get_max_col(sorted_data[0])
    row_start = 4
    col_start = 0

    unpack_columns = ['scoreArtistic', 'scoreExecution', 'scoreDifficulty', 'deduction']

    green_formats = []
    green_columns = ['meanArtistic', 'meanExecution', 'meanDifficult', 'sumDeduction', 'place']

    total_formats = []
    orange_columns = ['total']

    # write title
    title_style = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'font_size': 16})
    worksheet.merge_range(0, 0, 0, col_max - 1, 'Протокол соревнований', title_style)

    # write header
    # 1
    header_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True, })
    header_start = ['№', 'Фамилия Имя', 'Город']
    i = 0
    for h in header_start:
        worksheet.merge_range(row_start - 2, col_start + i, row_start - 1, col_start + i, h, header_format)
        i += 1

    # 2
    header_score = ['Артистизм', 'Исполнение', 'Сложность', 'Сбавки']
    col_next = len(header_start)
    col_prev = 0
    i = -1

    for h in header_score:
        data = sorted_data[0][unpack_columns[i + 1]]
        stepan = len(data)
        worksheet.merge_range(row_start - 2, col_start + col_next, row_start - 2, col_start + col_next + stepan, h, header_format)

        c = 0
        for k in data.keys():
            worksheet.write(1 + row_start - 2, c + col_start + col_next, k, header_format)
            # worksheet.set_column(1 + row_start - 2, c + col_start + col_next, 5) # resize cell
            c += 1

        worksheet.write(1 + row_start - 2, c + col_start + col_next, 'СР', header_format)

        i += 1
        col_prev = col_next
        col_next = col_prev + stepan + 1

    # 3
    header_end = ['Общий\nбалл', 'Место']
    i = 0
    for h in header_end:
        worksheet.merge_range(row_start - 2, col_start + col_next + i, row_start - 1, col_start + col_next + i, h, header_format)
        i += 1

    # data write
    for person in sorted_data:
        if person['total'] == 0:
            continue

        data = []

        for k, v in person.items():
            # style 1
            if k in orange_columns:
                total_formats.append({
                    "row": row_start,
                    "col": len(data),
                    "value": v,
                    "style": orange_style,
                })

            # style 2
            if k in green_columns:
                green_formats.append({
                    "row": row_start,
                    "col": len(data),
                    "value": v,
                    "style": green_style,
                })

            # cell unpack
            if k in unpack_columns:
                field = v.values()
                [data.append(i) for i in field]
                continue

            # simple cell
            data.append(v)

        # write row to file
        print(f'{data}')
        worksheet.write_row(row_start, col_start, data, default_style)
        worksheet.set_row(row_start, 30)
        row_start += 1
    # end

    # change style
    for x in green_formats:
        worksheet.write(x['row'], x['col'], x['value'], x['style'])

    for x in total_formats:
        worksheet.write(x['row'], x['col'], x['value'], x['style'])

    # change columns A, B, C width
    number_column_width = 5
    name_column_width = len(max(sorted_data, key=lambda o: len(o['name']))['name']) * 1.2
    city_column_width = len(max(sorted_data, key=lambda o: len(o['city']))['city']) * 1.2

    worksheet.set_column('A:A', number_column_width)
    worksheet.set_column('B:B', name_column_width)
    worksheet.set_column('C:C', city_column_width)
    
    # bottom sign
    sign_mid_style = workbook.add_format({'align': 'center', 'valign': 'bottom', 'font_size': 12})
    sign_left_style = workbook.add_format({'align': 'right', 'valign': 'bottom', 'font_size': 12})
    sign_right_style = workbook.add_format({'align': 'left', 'valign': 'bottom', 'font_size': 12})
    mid = col_next//2

    worksheet.write(row_max + 5, mid, '___________________', sign_mid_style)
    worksheet.write(row_max + 7, mid, '___________________', sign_mid_style)
    worksheet.write(row_max + 5, mid - 2, 'Главный судья соревнований', sign_left_style)
    worksheet.write(row_max + 7, mid - 2, 'Главный секретарь соревнований', sign_left_style)
    worksheet.write(row_max + 5, mid + 2, judge_name, sign_right_style)
    worksheet.write(row_max + 7, mid + 2, secretary_name, sign_right_style)

    # write all
    workbook.close()
