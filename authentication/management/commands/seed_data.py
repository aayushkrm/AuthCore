from django.core.management.base import BaseCommand
from authentication.models import User
from authorization.models import Role, BusinessElement, AccessRoleRule, UserRole
from django.db import transaction


class Command(BaseCommand):
    help = 'Seeds the database with initial test data for authentication and authorization'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Clearing existing data...'))
        
        # Clear existing data (in correct order due to foreign keys)
        AccessRoleRule.objects.all().delete()
        UserRole.objects.all().delete()
        BusinessElement.objects.all().delete()
        Role.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('✓ Data cleared'))
        self.stdout.write(self.style.SUCCESS('\nCreating roles...'))
        
        # ==================== CREATE ROLES ====================
        admin_role = Role.objects.create(
            name='admin',
            description='Full system administrator with all permissions'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created role: admin'))
        
        manager_role = Role.objects.create(
            name='manager',
            description='Manager with extended permissions'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created role: manager'))
        
        user_role = Role.objects.create(
            name='user',
            description='Regular user with basic permissions'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created role: user'))
        
        guest_role = Role.objects.create(
            name='guest',
            description='Guest user with read-only access'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created role: guest'))

        self.stdout.write(self.style.SUCCESS('\nCreating business elements...'))
        
        # ==================== CREATE BUSINESS ELEMENTS ====================
        products_elem = BusinessElement.objects.create(
            name='products',
            description='Product catalog management'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created element: products'))
        
        users_elem = BusinessElement.objects.create(
            name='users',
            description='User account management'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created element: users'))
        
        orders_elem = BusinessElement.objects.create(
            name='orders',
            description='Order management and tracking'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created element: orders'))
        
        stores_elem = BusinessElement.objects.create(
            name='stores',
            description='Store location management'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created element: stores'))
        
        access_rules_elem = BusinessElement.objects.create(
            name='access_rules',
            description='Access control rules management'
        )
        self.stdout.write(self.style.SUCCESS('  ✓ Created element: access_rules'))

        self.stdout.write(self.style.SUCCESS('\nCreating access rules...'))

        # ==================== ADMIN ROLE - Full access to everything ====================
        rule_count = 0
        for element in [products_elem, users_elem, orders_elem, stores_elem, access_rules_elem]:
            AccessRoleRule.objects.create(
                role=admin_role,
                element=element,
                read_permission=False,
                read_all_permission=True,
                create_permission=True,
                update_permission=False,
                update_all_permission=True,
                delete_permission=False,
                delete_all_permission=True
            )
            rule_count += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {rule_count} rules for admin'))

        # ==================== MANAGER ROLE - Extended permissions ====================
        rule_count = 0
        
        # Products: Full read, create, update all, but no delete
        AccessRoleRule.objects.create(
            role=manager_role,
            element=products_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=True,
            update_permission=False,
            update_all_permission=True,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Orders: Full read and update, limited delete
        AccessRoleRule.objects.create(
            role=manager_role,
            element=orders_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=True,
            update_permission=False,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Stores: Full read and create
        AccessRoleRule.objects.create(
            role=manager_role,
            element=stores_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Users: Read all only
        AccessRoleRule.objects.create(
            role=manager_role,
            element=users_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=False,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {rule_count} rules for manager'))

        # ==================== USER ROLE - Basic CRUD on own objects ====================
        rule_count = 0
        
        # Products: CRUD on own products
        AccessRoleRule.objects.create(
            role=user_role,
            element=products_elem,
            read_permission=True,
            read_all_permission=False,
            create_permission=True,
            update_permission=True,
            update_all_permission=False,
            delete_permission=True,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Orders: CRUD on own orders
        AccessRoleRule.objects.create(
            role=user_role,
            element=orders_elem,
            read_permission=True,
            read_all_permission=False,
            create_permission=True,
            update_permission=True,
            update_all_permission=False,
            delete_permission=True,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Stores: Read all stores
        AccessRoleRule.objects.create(
            role=user_role,
            element=stores_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=False,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {rule_count} rules for user'))

        # ==================== GUEST ROLE - Read-only access ====================
        rule_count = 0
        
        # Products: Read all
        AccessRoleRule.objects.create(
            role=guest_role,
            element=products_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=False,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        # Stores: Read all
        AccessRoleRule.objects.create(
            role=guest_role,
            element=stores_elem,
            read_permission=False,
            read_all_permission=True,
            create_permission=False,
            update_permission=False,
            update_all_permission=False,
            delete_permission=False,
            delete_all_permission=False
        )
        rule_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {rule_count} rules for guest'))

        self.stdout.write(self.style.SUCCESS('\nCreating test users...'))

        # ==================== CREATE TEST USERS ====================
        
        # Admin user
        admin_user = User.objects.create(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            patronymic='Administrator'
        )
        admin_user.set_password('password123')
        admin_user.save()
        UserRole.objects.create(user=admin_user, role=admin_role)
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: admin@test.com'))

        # Manager user
        manager_user = User.objects.create(
            email='manager@test.com',
            first_name='Manager',
            last_name='User',
            patronymic='Management'
        )
        manager_user.set_password('password123')
        manager_user.save()
        UserRole.objects.create(user=manager_user, role=manager_role)
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: manager@test.com'))

        # Regular user 1
        regular_user1 = User.objects.create(
            email='user1@test.com',
            first_name='John',
            last_name='Doe',
            patronymic='Michael'
        )
        regular_user1.set_password('password123')
        regular_user1.save()
        UserRole.objects.create(user=regular_user1, role=user_role)
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: user1@test.com'))

        # Regular user 2
        regular_user2 = User.objects.create(
            email='user2@test.com',
            first_name='Jane',
            last_name='Smith',
            patronymic='Elizabeth'
        )
        regular_user2.set_password('password123')
        regular_user2.save()
        UserRole.objects.create(user=regular_user2, role=user_role)
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: user2@test.com'))

        # Guest user
        guest_user = User.objects.create(
            email='guest@test.com',
            first_name='Guest',
            last_name='User',
            patronymic=''
        )
        guest_user.set_password('password123')
        guest_user.save()
        UserRole.objects.create(user=guest_user, role=guest_role)
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: guest@test.com'))

        # Inactive user for testing soft delete
        inactive_user = User.objects.create(
            email='inactive@test.com',
            first_name='Inactive',
            last_name='User',
            patronymic='',
            is_active=False
        )
        inactive_user.set_password('password123')
        inactive_user.save()
        self.stdout.write(self.style.SUCCESS('  ✓ Created user: inactive@test.com (deactivated)'))

        # Print summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('DATABASE SEEDED SUCCESSFULLY!'))
        self.stdout.write('='*60)
        
        self.stdout.write(self.style.WARNING('\n📊 Summary:'))
        self.stdout.write(f'  • Roles: {Role.objects.count()}')
        self.stdout.write(f'  • Business Elements: {BusinessElement.objects.count()}')
        self.stdout.write(f'  • Access Rules: {AccessRoleRule.objects.count()}')
        self.stdout.write(f'  • Users: {User.objects.count()}')
        self.stdout.write(f'  • User-Role Assignments: {UserRole.objects.count()}')
        
        self.stdout.write(self.style.WARNING('\n🔑 Test Accounts (all passwords: password123):'))
        self.stdout.write(self.style.SUCCESS('  • admin@test.com      - Full system access'))
        self.stdout.write(self.style.SUCCESS('  • manager@test.com    - Extended permissions'))
        self.stdout.write(self.style.SUCCESS('  • user1@test.com      - Basic user access'))
        self.stdout.write(self.style.SUCCESS('  • user2@test.com      - Basic user access'))
        self.stdout.write(self.style.SUCCESS('  • guest@test.com      - Read-only access'))
        self.stdout.write(self.style.WARNING('  • inactive@test.com   - Deactivated (cannot login)'))
        
        self.stdout.write('\n' + '='*60 + '\n')
