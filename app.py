import os
import asyncio
import mimetypes
import tornado
import tornado.options
import markdown
from tornado.web import StaticFileHandler, RequestHandler

tornado.options.options.log_file_prefix = "tornado_application_access_log.log"
tornado.options.parse_command_line()

supported_mime_types = {
	'.markdown': 'text/markdown',
	'.md': 'text/markdown',
	'.mjs': 'application/javascript',
	'.webmanifest': 'application/manifest+json',
	'.ico': 'image/x-icon',
	'.webp': 'image/webp',
	'.wasm': 'application/wasm',
	'.mp4': 'video/mp4',
	'.webm': 'video/webm',
	'.ogv': 'video/ogg',
	'.mp3': 'audio/mpeg',
	'.wav': 'audio/wav',
	'.ogg': 'audio/ogg',
	'.pdf': 'application/pdf',
	'.epub': 'application/epub+zip',
	'.zip': 'application/zip',
	'.tar': 'application/x-tar',
	'.gz': 'application/gzip',
	'.xml': 'application/xml',
	'.yaml': 'application/yaml',
	'.yml': 'application/yaml',
	'.toml': 'application/toml',
	'.csv': 'text/csv',
	'.tsv': 'text/tab-separated-values',
	'.geojson': 'application/geo+json',
}

for ext, mime in supported_mime_types.items():
	mimetypes.add_type(mime, ext)


class CustomRedirectHandler(RequestHandler):
	def get(self, path):
		try:
			if path in ["", "index"]:
				self.render("static_site/index.html")
				return

			if path.endswith('.md'):
				file_path = os.path.join(os.getcwd(), "static_site", path)
				if os.path.exists(file_path):
					self.set_header("Content-Type", "text/html; charset=UTF-8")
					with open(file_path, "r", encoding="utf-8") as md_file:
						md_content = md_file.read()
						html_content = self.convert_markdown_to_html(md_content)
						self.write(html_content)
					return
				else:
					self.send_error(404)
					return

			if path.endswith('.html'):
				clean_path = path[:-5]
				self.redirect(f'/{clean_path}')
				return

			file_path = os.path.join(os.getcwd(), "static_site", path)
			if os.path.exists(file_path):
				ext = os.path.splitext(file_path)[1]
				mime_type, _ = mimetypes.guess_type(file_path)
				self.set_header("Content-Type", mime_type or "application/octet-stream")
				with open(file_path, "rb") as file:
					self.write(file.read())
			else:
				html_file_path = f"{file_path}.html"
				if os.path.exists(html_file_path):
					self.set_header("Content-Type", "text/html; charset=UTF-8")
					with open(html_file_path, "r", encoding="utf-8") as file:
						self.write(file.read())
				else:
					self.send_error(404)
		except Exception as e:
			self.send_error(500, reason=str(e))

	def convert_markdown_to_html(self, md_content):
		html_content = markdown.markdown(md_content)
		html_page = f"""
		<!DOCTYPE html>
		<html lang="en">
		<head>
			<meta charset="UTF-8">
			<meta name="viewport" content="width=device-width, initial-scale=1.0">
			<style>
				body {{
					font-family: monospace;
					line-height: 1.7;
					margin: 0;
					padding: 20px;
					background-color: black;
					color: #abb2bf;
					font-size: 15px;
					display:flex:
					align-items:center;
					justify-content:center;
				}}

				h1, h2, h3, h4, h5, h6 {{
					margin: 1.5em 0 0.5em;
					font-weight: bold;
					color: #61dafb;
					line-height: 1.3;
				}}
				h1 {{
					font-size: 2.2em;
					border-bottom: 2px solid #61dafb;
					padding-bottom: 0.3em;
				}}
				h2 {{
					font-size: 1.8em;
					border-bottom: 1px solid #61dafb;
					padding-bottom: 0.2em;
				}}
				h3 {{
					font-size: 1.5em;
				}}

				p {{
					margin-bottom: 1em;
					color: #dcdcdc;
				}}

				a {{
					color: #61dafb;
					text-decoration: none;
				}}
				a:hover {{
					text-decoration: underline;
				}}

				ul, ol {{
					margin: 0 0 1.5em 1.5em;
					padding: 0;
				}}
				ul li, ol li {{
					margin-bottom: 0.5em;
				}}



				code {{
					display:relative;
					background-color: #1e222a;
					padding: 3px 6px;
					border-radius: 4px;
					color: #e06c75;
					white-space: pre-wrap;
					font-size: 0.95em;
				}}
				pre {{
					background-color: #1e222a;
					padding: 20px;
					border-radius: 6px;
					overflow-x: auto;
					line-height: 1.45;
					font-size: 0.95em;
					margin: 1.5em 0;
					color: #abb2bf;
					border: 1px solid #3e4451;
				}}
				pre code {{
					background-color: transparent;
					border: none;
					padding: 0;
					color: inherit;
				}}


				blockquote {{
					margin: 1.5em 0;
					padding: 1em;
					color: #d19a66;
					border-left: 4px solid #c678dd;
					background-color: #1e222a;
					border-radius: 4px;
				}}
				blockquote p {{
					margin: 0;
				}}

				.command-line {{
					font-family: "Fira Code", monospace;
					font-size: 0.95em;
					background-color: #1e222a;
					padding: 15px;
					border-radius: 6px;
					color: #98c379;
					white-space: pre-wrap;
					overflow-x: auto;
					margin: 1em 0;
				}}
				.command-line span {{
					color: #61dafb;
				}}

				table {{
					width: 100%;
					border-collapse: collapse;
					margin: 1.5em 0;
					background-color: #1e222a;
					border: 1px solid #3e4451;
					color: #abb2bf;
				}}
				th, td {{
					padding: 10px 15px;
					border: 1px solid #3e4451;
					text-align: left;
				}}
				th {{
					background-color: #3e4451;
					font-weight: bold;
					color: #61dafb;
				}}

				img {{
					max-width: 100%;
					height: auto;
					display: block;
					margin: 1.5em 0;
					border-radius: 4px;
				}}
			</style>
		</head>
		<body>
			{html_content}
		</body>
		</html>
		"""
		return html_page





def make_app():
	return tornado.web.Application([
		(r"/(.*)", CustomRedirectHandler),
	], debug=True)


async def main():
	app = make_app()
	port = 5000
	address = "127.0.0.1"
	app.listen(port, address)
	print(f"Server is running on http://{address}:{port}")
	await asyncio.Event().wait()


if __name__ == "__main__":
	asyncio.run(main())
