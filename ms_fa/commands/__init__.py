import typer
from typing import Optional

from ms_fa.db import SessionLocal, engine, Base
from ms_fa.db.seeders import SEEDERS
from ms_fa.models import *  # Import all models to register them

app = typer.Typer(help="MS Users FastAPI CLI commands")


@app.command()
def seed(
    seeder: Optional[str] = typer.Option(
        None,
        "--seeder", "-s",
        help="Run a specific seeder by name (e.g., PermissionSeeder)"
    ),
    fresh: bool = typer.Option(
        False,
        "--fresh", "-f",
        help="Drop all tables and recreate them before seeding"
    )
):
    """
    Run database seeders.
    
    Examples:
        python -m ms_fa.commands seed
        python -m ms_fa.commands seed --seeder PermissionSeeder
        python -m ms_fa.commands seed --fresh
    """
    db = SessionLocal()
    
    try:
        if fresh:
            typer.echo("🗑️  Dropping all tables...")
            Base.metadata.drop_all(bind=engine)
            typer.echo("✨ Creating all tables...")
            Base.metadata.create_all(bind=engine)
        
        typer.echo("\n🌱 Running seeders...\n")
        
        # Sort seeders by priority
        sorted_seeders = sorted(SEEDERS, key=lambda s: s.priority)
        
        for seeder_class in sorted_seeders:
            # If a specific seeder is requested, skip others
            if seeder and seeder_class.__name__ != seeder:
                continue
            
            typer.echo(f"📦 Running {seeder_class.__name__}...")
            seeder_instance = seeder_class(db)
            seeder_instance.run()
        
        typer.echo("\n✅ Seeding completed successfully!\n")
        
    except Exception as e:
        db.rollback()
        typer.echo(f"\n❌ Error: {e}\n", err=True)
        raise typer.Exit(1)
    finally:
        db.close()


@app.command()
def create_tables():
    """
    Create all database tables.
    
    Example:
        python -m ms_fa.commands create-tables
    """
    typer.echo("✨ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    typer.echo("✅ Tables created successfully!")


@app.command()
def drop_tables():
    """
    Drop all database tables.
    
    Example:
        python -m ms_fa.commands drop-tables
    """
    confirm = typer.confirm("⚠️  Are you sure you want to drop all tables?")
    if confirm:
        typer.echo("🗑️  Dropping all tables...")
        Base.metadata.drop_all(bind=engine)
        typer.echo("✅ Tables dropped successfully!")
    else:
        typer.echo("Operation cancelled.")


@app.command()
def createsuperuser(
    email: str = typer.Option(..., prompt=True, help="Admin email"),
    phone: str = typer.Option(..., prompt=True, help="Admin phone"),
    password: str = typer.Option(
        ..., 
        prompt=True, 
        confirmation_prompt=True, 
        hide_input=True,
        help="Admin password"
    ),
    name: str = typer.Option("Admin", help="Admin name"),
):
    """
    Create a superuser (root) account.
    
    Example:
        python -m ms_fa.commands createsuperuser
    """
    from ms_fa.models import User, Role
    
    db = SessionLocal()
    
    try:
        # Check if user already exists
        existing = db.query(User).filter(
            (User.email == email) | (User.phone == phone)
        ).first()
        
        if existing:
            typer.echo(f"❌ User with email '{email}' or phone '{phone}' already exists!")
            raise typer.Exit(1)
        
        # Get root role
        root_role = db.query(Role).filter_by(name="root").first()
        
        if not root_role:
            typer.echo("❌ Root role not found. Please run seeders first!")
            raise typer.Exit(1)
        
        # Create user
        user = User({
            "email": email,
            "phone": phone,
            "name": name,
        })
        user.is_active = True
        user.set_password(password)
        user.roles.append(root_role)
        
        db.add(user)
        db.commit()
        
        typer.echo(f"\n✅ Superuser created successfully!")
        typer.echo(f"   Email: {email}")
        typer.echo(f"   Phone: {phone}\n")
        
    except Exception as e:
        db.rollback()
        typer.echo(f"\n❌ Error: {e}\n", err=True)
        raise typer.Exit(1)
    finally:
        db.close()


def main():
    app()


if __name__ == "__main__":
    main()
