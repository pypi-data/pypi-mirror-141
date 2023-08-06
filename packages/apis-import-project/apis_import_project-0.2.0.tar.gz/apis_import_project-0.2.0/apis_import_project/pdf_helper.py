# import fitz
# from tempfile import TemporaryFile
# from PIL import Image
# from .models import DataSource, DataSourcePage, ImportProject
# from django.core.files.storage import default_storage
# import io
#
#
# # todo implementd ziped jpeg folder upload
# def create_pdf_object(data):
#     # depending on the size of the uploaded file, django stores it either in memory or as a temp-file
#     # behaviour could be overwritten by specifying an upload handler
#     if data.__class__.__name__ == "_TemporaryFileWrapper":
#         pdf_obj = fitz.open(data)
#     else:
#         pdf_obj = fitz.open(stream=data, filetype="pdf")
#
#     return pdf_obj
#
# def process_pdf(filestream, name, citation, project_pk, owner, year=None):
#     # create pymupdf object and convert this object to images, and save the metadata in db
#     pdf_obj = create_pdf_object(filestream.file)
#     ds_pk = convert_pdf_to_images(pdf_obj, name, citation, year, project_pk, owner)
#
#     return ds_pk
#
#
# def convert_pdf_to_images(pdf_obj, pdf_name, citation, year, project_pk, owner):
#     # converts the pdf_obj into png files
#     ds = create_data_source_object(pdf_name, citation, owner)
#     if year:
#         ds.year = year
#         ds.save()
#
#
#
#     for index, page in enumerate(pdf_obj):
#         page_num = index+1
#         print(f"processing page {page_num}")
#         page_token = str(page_num)
#         img = page.get_pixmap(dpi=300)
#
#         """
#         # consider using something like this to crop the center of the image with pil
#
#         """
#
#
#         def crop_center(pil_img, crop_width, crop_height):
#             img_width, img_height = pil_img.size
#             return pil_img.crop(((img_width - crop_width) // 2,
#                                  (img_height - crop_height) // 2,
#                                  (img_width + crop_width) // 2,
#                                  (img_height + crop_height) // 2))
#
#         imgbytes = img.tobytes()
#         pseudo_file = io.BytesIO(imgbytes)
#
#         w, h = img.width, img.height
#
#         pil_img = Image.open(pseudo_file)
#         pil_cropped = crop_center(pil_img, 1500, 1500)
#         pil_cropped.thumbnail((500, 500), Image.ANTIALIAS)
#         pil_cropped = pil_cropped.resize((200, 200))
#
#
#         square_thumb = io.BytesIO()
#         pil_cropped.save(square_thumb, format='PNG')
#
#         # png files get stored at the default storage location
#         page_path = f"{pdf_name}_page_{page_num}.png"
#         default_storage.save(page_path, pseudo_file) #todo refactor: use image field correctly to save image and get rid of path
#         page_obj, created = DataSourcePage.objects.get_or_create(DataSource=ds, page_index=page_num, page_token=page_token)
#         page_obj.image = page_path
#         page_obj.thumbnail.save(page_path.replace(".png", "thumbnail.png"), square_thumb)
#         page_obj.save()
#
#     page_count = page_num
#     ds.page_count = page_count
#     ds.save()
#
#     project = ImportProject.objects.get(pk=int(project_pk))
#     project.DataSources.add(ds)
#
#     # metadata of the source is saved to db
#     return ds.pk
#
# def create_data_source_object(name, citation, owner):
#     path = default_storage.base_location + name
#     ds, created = DataSource.objects.get_or_create(name=name, path=path, citation=citation, owner=owner)
#
#     return ds
#
#
#
#
