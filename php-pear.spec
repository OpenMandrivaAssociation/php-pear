%define	_requires_exceptions pear(\\(PHPUnit.*\\|PEAR.*\\))
%define Archive_Tar_version 1.3.7
%define Console_Getopt_version 1.3.0
%define Structures_Graph_version 1.0.4
%define XML_RPC_version 1.5.4
%define XML_Util_version 1.2.1

Summary:	PHP Extension and Application Repository
Name:		php-pear
Version:	1.9.2
Epoch:      1
Release:	%mkrel 1
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PEAR/
Source0:	http://pear.php.net/get/PEAR-%{version}.tgz
Source1:    install-pear.php
Source2:    relocate.php
Source3:    strip.php
Source4:    LICENSE
Source5:    pear.script
Source10:   pear.sh
Source11:   pecl.sh
Source12:   peardev.sh
Source20:   http://pear.php.net/get/XML_RPC-%{XML_RPC_version}.tgz
Source21:   http://pear.php.net/get/Archive_Tar-%{Archive_Tar_version}.tgz
Source22:   http://pear.php.net/get/Console_Getopt-%{Console_Getopt_version}.tgz
Source23:   http://pear.php.net/get/Structures_Graph-%{Structures_Graph_version}.tgz
Source24:   http://pear.php.net/get/XML_Util-%{XML_Util_version}.tgz
BuildRequires:	php-cli
BuildRequires:	php-xml
Requires:	php-cli
Requires:	php-xml
Provides:   php-pear-Console_Getopt = %{Console_Getopt_version}
Provides:   php-pear-Archive_Tar = %{Archive_Tar_version}
Provides:   php-pear-Structures_Graph = %{Structures_Graph_version}
Provides:   php-pear-XML_RPC = %{XML_RPC_version}
Provides:   php-pear-XML_Util = %{XML_Util_version}
Obsoletes:	php-pear-XML_Util < %{XML_Util_version}
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
PEAR is short for "PHP Extension and Application Repository" and is pronounced
just like the fruit. The purpose of PEAR is to provide:

 * A structured library of open-sourced code for PHP users
 * A system for code distribution and package maintenance
 * A standard style for code written in PHP
 * The PHP Foundation Classes (PFC)
 * The PHP Extension Code Library (PECL)
 * A web site, mailing lists and download mirrors to support the PHP/PEAR
   community

%prep
%setup -q -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}; do
    tar xzf  $archive --strip-components 1
done
tar xzf %{SOURCE24} package.xml
mv package.xml XML_Util.xml

%build

%install
rm -rf %{buildroot}

export PHP_PEAR_SYSCONF_DIR=%{_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{_datadir}/pear

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d \
    %{buildroot}%{_datadir}/pear \
    %{buildroot}%{_localstatedir}/cache/php-pear \
    %{buildroot}%{_localstatedir}/www/html \
    %{buildroot}%{_datadir}/pear/.pkgxml \
    %{buildroot}%{_sysconfdir}/rpm \
    %{buildroot}%{_sysconfdir}/pear

export INSTALL_ROOT=%{buildroot}

%{_bindir}/php \
    -n -dmemory_limit=32M -dshort_open_tag=0 -dsafe_mode=0 \
    -derror_reporting=E_ALL -ddetect_unicode=0 \
    %{SOURCE1} -d %{_datadir}/pear \
    -c %{_sysconfdir}/pear \
    -b %{_bindir} \
    -w %{_localstatedir}/www/html \
    %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE20}

# Replace /usr/bin/* with simple scripts:
install -m 755 %{SOURCE10} %{buildroot}%{_bindir}/pear
install -m 755 %{SOURCE11} %{buildroot}%{_bindir}/pecl
install -m 755 %{SOURCE12} %{buildroot}%{_bindir}/peardev

# Sanitize the pear.conf
%{_bindir}/php -n %{SOURCE2} %{buildroot}%{_sysconfdir}/pear.conf %{buildroot} | 
%{_bindir}/php -n %{SOURCE2} php://stdin $PWD > new-pear.conf
%{_bindir}/php -n %{SOURCE3} new-pear.conf ext_dir |
%{_bindir}/php -n %{SOURCE3} php://stdin http_proxy > %{buildroot}%{_sysconfdir}/pear.conf

%{_bindir}/php -r "print_r(unserialize(substr(file_get_contents('%{buildroot}%{_sysconfdir}/pear.conf'),17)));"

install -m 644 -c %{SOURCE4} LICENSE

# Why this file here ?
rm -rf %{buildroot}/.depdb* %{buildroot}/.lock %{buildroot}/.channels %{buildroot}/.filemap

# Need for re-registrying XML_Util
install -m 644 XML_Util.xml %{buildroot}%{_datadir}/pear/.pkgxml/

# rpm filetriggers
install -d -m 755 %{buildroot}%{_localstatedir}/lib/rpm/filetriggers
cat > %buildroot%{_localstatedir}/lib/rpm/filetriggers/pear.filter << EOF
^.%{_datadir}/pear/packages/.*\.xml$
EOF
install -m 755 %{SOURCE5} \
    %{buildroot}%{_localstatedir}/lib/rpm/filetriggers/pear.script

%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep %{buildroot} %{buildroot}%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} %{buildroot}%{_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' %{buildroot}%{_sysconfdir}/pear.conf && exit 1
grep /usr/local %{buildroot}%{_sysconfdir}/pear.conf && exit 1
grep -rl %{buildroot} %{buildroot} && exit 1

%clean
rm -rf %{buildroot}

%triggerpostun -- php-pear-XML-Util
# re-register extension unregistered during postun of obsoleted
# package php-pear-XML-Util
%{_bindir}/pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/XML_Util.xml >/dev/null || :

%files
%defattr(-,root,root)
%doc LICENSE README
%dir %{_sysconfdir}/pear
%config(noreplace) %{_sysconfdir}/pear.conf
%{_datadir}/pear
%{_bindir}/*
%dir %{_localstatedir}/cache/php-pear
%{_localstatedir}/lib/rpm/filetriggers/pear.*
