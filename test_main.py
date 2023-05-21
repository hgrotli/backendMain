def upload():
    if request.method == "POST":
        file = request.files["file"]
        file_content = file.read().decode("utf-8")
        text = vobject.readComponents(file_content)
        for dataContact in text:
            phone = "--No Information--"
            try:
                phone = str(dataContact.tel.value)
            except AttributeError:
                pass
            address = "--No Information--"
            try:
                address = str(dataContact.adr.value)
            except AttributeError:
                pass
            company = "--No Information--"
            try:
                company = str(dataContact.org.value[0])
            except AttributeError:
                pass

            MyContact = {
                "email": dataContact.email.value,
                "name": str(dataContact.n.value),
                "fullname": dataContact.fn.value,
                "address": address,
                "company": company,
                "phone": phone,
            }

            result = mycol.insert_one(MyContact)
            MyData.append(str(result.inserted_id))
            print(MyContact)

            # Trigger an update request to the cache server
        cache_url = "https://asi2-cache2.onrender.com/update_cache"
        response = requests.get(cache_url)
        return jsonify({"message": MyData})

    else:
        # show the upload form
        return render_template("upload.html")