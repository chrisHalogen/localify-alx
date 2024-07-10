from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


# postgresql://localifydb_user:J98IICExHVgCoSsvDClgmY8EBPjebtTO@dpg-cq6qelmehbks73fkpb2g-a.oregon-postgres.render.com/localifydb
