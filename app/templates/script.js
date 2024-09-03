document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const navIcons = document.querySelectorAll('.nav-icon');
    
    // User Profile Menu Functionality
    const userProfile = document.querySelector('.user-profile');
    const userMenu = document.querySelector('.user-menu');
    
    userProfile.addEventListener('click', function(e) {
        e.stopPropagation();
        this.classList.toggle('active');
        userMenu.classList.toggle('active');
    });

    document.addEventListener('click', function(e) {
        if (!userProfile.contains(e.target)) {
            userProfile.classList.remove('active');
            userMenu.classList.remove('active');
        }
    });

    function toggleSidebar() {
        sidebar.classList.toggle('show');
        
        if (window.innerWidth < 768) {
            if (sidebar.classList.contains('show')) {
                mainContent.style.marginLeft = '250px';
            } else {
                mainContent.style.marginLeft = '0';
            }
        }
    }

    sidebarToggle.addEventListener('click', toggleSidebar);

    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            sidebar.classList.remove('show');
            mainContent.style.marginLeft = '250px';
        } else {
            mainContent.style.marginLeft = sidebar.classList.contains('show') ? '250px' : '0';
        }
    });

    // Inicialização
    if (window.innerWidth >= 768) {
        mainContent.style.marginLeft = '250px';
    } else {
        mainContent.style.marginLeft = '0';
    }

    // Adicionar funcionalidade para alternar entre listas
    navIcons.forEach(icon => {
        icon.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover classe 'active' de todos os ícones e adicionar ao clicado
            navIcons.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Esconder todas as listas e mostrar a selecionada
            const targetId = this.getAttribute('data-target');
            document.querySelectorAll('.chat-list').forEach(list => {
                list.classList.remove('active');
            });
            document.getElementById(targetId).classList.add('active');
        });
    });
    
});
