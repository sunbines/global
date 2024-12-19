%if 0%{?fedora} >= 15 || 0%{?rhel} >= 7 || 0%{?openEuler}
%bcond_with xemacs
%else
%bcond_without xemacs
%endif

Name:           global
Version:        6.6.13
Release:        4%{?dist}
Summary:        Source code tag system
Group:          Development/Tools
# The entire source code is GPLv3+ except
#   libglibc/ which is LGPLv2+
#   gtags-cscope/ which is BSD
#   libparser/ which is GPLv2+
#   jquery/ which is MIT
License:        GPLv3+ and LGPLv2+ and BSD and GPLv2+ and MIT
URL:            http://www.gnu.org/software/global
Source:         ftp://ftp.gnu.org/pub/gnu/global/global-%{version}.tar.gz
BuildRequires:  ncurses-devel, ctags-etags
BuildRequires:  libtool-ltdl-devel
%if 0%{?rhel} == 7
BuildRequires:  python%{python3_pkgversion}-devel
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  emacs
%if %{with xemacs}
BuildRequires:  xemacs
Requires:       xemacs-filesystem >= %{_xemacs_version}
%endif
Requires:       emacs-filesystem >= %{_emacs_version}
Obsoletes:      emacs-global <= 6.5.1-1
Obsoletes:      emacs-global-el <= 6.5.1-1
Provides:       emacs-global = %{version}-%{release}
Provides:       emacs-global-el = %{version}-%{release}

%description
GNU GLOBAL is a source code tag system that works the same way across
diverse environments. It supports C, C++, Yacc, Java, PHP and
assembler source code.

%package        ctags
Summary:        Integration of Exuberant Ctags and Pygments with GLOBAL
License:        GPLv3+
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}, ctags-etags
%if 0%{?rhel} == 7
Requires:       python%{python3_pkgversion}-pygments
%else
Requires:       python3-pygments
%endif

%description    ctags
This package contains plug-ins that provides support for more languages
through Pygments and Exuberant Ctags.

%prep
%setup -q

%build
export PYTHON=%{__python3}
%configure --with-posix-sort=/bin/sort --with-exuberant-ctags=/bin/ctags --localstatedir=/var/tmp/  --without-included-ltdl
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Remove empty useless directory
rm -f %{buildroot}%{_infodir}/dir

rm -f %{buildroot}%{_libdir}/gtags/*.*a
rm -f %{buildroot}%{_libdir}/gtags/user-custom.*

rm %{buildroot}/%{_datadir}/gtags/{gtags.el,gtags.conf}
rm %{buildroot}/%{_datadir}/gtags/{AUTHORS,COPYING,ChangeLog,DONORS,FAQ,INSTALL,LICENSE,NEWS,README,THANKS}

# fix rpmlint error
chmod +x %{buildroot}/%{_datadir}/gtags/{global,completion}.cgi

mkdir -p %{buildroot}%{_sysconfdir}
install gtags.conf -t %{buildroot}%{_sysconfdir}

mkdir -p %{buildroot}%{_emacs_sitelispdir}
install gtags.el -p -t %{buildroot}%{_emacs_sitelispdir}
%{_emacs_bytecompile} %{buildroot}%{_emacs_sitelispdir}/gtags.el
chmod -x %{buildroot}%{_emacs_sitelispdir}/gtags.el
%if %{with xemacs}
mkdir -p %{buildroot}%{_xemacs_sitelispdir}
install gtags.el -p -t %{buildroot}%{_xemacs_sitelispdir}
%{_xemacs_bytecompile} %{buildroot}%{_xemacs_sitelispdir}/gtags.el
chmod -x %{buildroot}%{_xemacs_sitelispdir}/gtags.el
%endif

## Remove executable flag
chmod -x %{buildroot}/%{_sysconfdir}/gtags.conf

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%files
%doc README THANKS AUTHORS FAQ NEWS
%doc DONORS ChangeLog
%license LICENSE COPYING
%config(noreplace) %{_sysconfdir}/gtags.conf
%{_bindir}/*
%{_infodir}/global.info*
%{_mandir}/man*/*
%{_datadir}/gtags
%{_emacs_sitelispdir}/gtags.el*
%if %{with xemacs}
%{_xemacs_sitelispdir}/gtags.el*
%endif


%files ctags
%dir %{_libdir}/gtags
%{_libdir}/gtags/*

%changelog