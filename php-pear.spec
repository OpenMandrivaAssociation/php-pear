%define		_requires_exceptions pear(../PEAR/RunTest.php)\\|pear(PHPUnit.php)

%define 	_PEAR_version 1.6.1
%define 	_Archive_Tar_version 1.3.2
%define 	_Console_Getopt_version 1.2.3
%define 	_Structures_Graph_version 1.0.2
%define 	_DB_version 1.7.11
%define 	_Log_version 1.9.11
%define 	_Mail_version 1.1.14
%define 	_Mail_Mime_version 1.5.2
%define 	_Mail_mimeDecode_version 1.5.0
%define 	_Net_SMTP_version 1.2.10
%define 	_Net_Socket_version 1.0.8
%define 	_XML_Parser_version 1.2.8
%define 	_XML_RPC_version 1.5.1

%define 	_pear_packages PEAR Archive_Tar Console_Getopt Structures_Graph DB Log Mail Mail_mimeDecode Mail_Mime Net_Socket Net_SMTP XML_Parser XML_RPC

Summary:	PEAR - PHP Extension and Application Repository
Name:		php-pear
Version:	5.2.3
Release:	%mkrel 4
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PEAR/
Source0:	http://pear.php.net/get/PEAR-%{_PEAR_version}.tar.bz2
Source1:	http://pear.php.net/get/Archive_Tar-%{_Archive_Tar_version}.tar.bz2
Source2:	http://pear.php.net/get/Console_Getopt-%{_Console_Getopt_version}.tar.bz2
Source3:	http://pear.php.net/get/DB-%{_DB_version}.tar.bz2
Source4:	http://pear.php.net/get/Log-%{_Log_version}.tar.bz2
Source5:	http://pear.php.net/get/Mail-%{_Mail_version}.tar.bz2
Source6:	http://pear.php.net/get/Mail_Mime-%{_Mail_Mime_version}.tar.bz2
Source7:	http://pear.php.net/get/Mail_mimeDecode-%{_Mail_mimeDecode_version}.tar.bz2
Source8:	http://pear.php.net/get/Net_SMTP-%{_Net_SMTP_version}.tar.bz2
Source9:	http://pear.php.net/get/Net_Socket-%{_Net_Socket_version}.tar.bz2
Source10:	http://pear.php.net/get/XML_Parser-%{_XML_Parser_version}.tar.bz2
Source11:	http://pear.php.net/get/XML_RPC-%{_XML_RPC_version}.tar.bz2
Source12:	http://pear.php.net/get/Structures_Graph-%{_Structures_Graph_version}.tar.bz2
Source20:	fixregistry.php
Provides:	pear = %{version}
Provides:	php-pear-PEAR = %{_PEAR_version}
Provides:	php-pear-PEAR-Command = %{_PEAR_version}
Provides:	php-pear-PEAR-Frontend_CLI = %{_PEAR_version}
Provides:	php-pear-PEAR-OS = %{_PEAR_version}
Provides:	php-pear-Archive_Tar = %{_Archive_Tar_version}
Provides:	php-pear-Console_Getopt = %{_Console_Getopt_version}
Provides:	php-pear-DB  = %{_DB_version}
Provides:	php-pear-Log = %{_Log_version}
Provides:	php-pear-Mail = %{_Mail_version}
Provides:	php-pear-Mail_Mime = %{_Mail_Mime_version}
Provides:	php-pear-Mail_mimeDecode = %{_Mail_mimeDecode_version}
Provides:	php-pear-Net_SMTP = %{_Net_SMTP_version}
Provides:	php-pear-Net_Socket = %{_Net_Socket_version}
Provides:	php-pear-XML_Parser = %{_XML_Parser_version}
Provides:	php-pear-XML_RPC = %{_XML_RPC_version}
Provides:	php-pear-Structures_Graph = %{_Structures_Graph_version}
Requires(post): php-cli php-pcre php-xml php-xmlrpc hping2
Requires(preun): php-cli php-pcre php-xml php-xmlrpc hping2
Requires:	php-cli php-pcre php-xml php-xmlrpc
Requires:	hping2
BuildRequires:	dos2unix
BuildRequires:	php-cli php-pcre php-xml php-xmlrpc
Obsoletes:	php-pear-PEAR
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend_CLI
Obsoletes:	php-pear-PEAR-OS
Obsoletes:	php-pear-Archive_Tar
Obsoletes:	php-pear-Console_Getopt
Obsoletes:	php-pear-DB
Obsoletes:	php-pear-Log
Obsoletes:	php-pear-Mail
Obsoletes:	php-pear-Mail_Mime
Obsoletes:	php-pear-Mail_mimeDecode
Obsoletes:	php-pear-Net_SMTP
Obsoletes:	php-pear-Net_Socket
Obsoletes:	php-pear-XML_Parser
Obsoletes:	php-pear-XML_RPC
Obsoletes:	php-pear-Structures_Graph
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
PEAR is short for "PHP Extension and Application Repository" and is pronounced
just like the fruit. The purpose of PEAR is to provide:

 * A structured library of open-sourced code for PHP users
 * A system for code distribution and package maintenance
 * A standard style for code written in PHP, specified here
 * The PHP Foundation Classes (PFC), see more below
 * The PHP Extension Code Library (PECL), see more below
 * A web site, mailing lists and download mirrors to support the PHP/PEAR
   community

%prep

%setup -q -c

mv package.xml PEAR.xml

tar -jxf %{SOURCE1}
mv package.xml Archive_Tar.xml

tar -jxf %{SOURCE2}
mv package.xml Console_Getopt.xml

tar -jxf %{SOURCE3}
mv package.xml DB.xml

tar -jxf %{SOURCE4}
mv package.xml Log.xml

tar -jxf %{SOURCE5}
mv package.xml Mail.xml

tar -jxf %{SOURCE6}
mv package.xml Mail_Mime.xml

tar -jxf %{SOURCE7}
mv package.xml Mail_mimeDecode.xml

tar -jxf %{SOURCE8}
mv package.xml Net_SMTP.xml

tar -jxf %{SOURCE9}
mv package.xml Net_Socket.xml

tar -jxf %{SOURCE10}
mv package.xml XML_Parser.xml

tar -jxf %{SOURCE11}
mv package.xml XML_RPC.xml

tar -jxf %{SOURCE12}
mv package.xml Structures_Graph.xml

# cleanup
rm -f package*.xml

cp %{SOURCE20} fixregistry.php

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/pearkeys
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_var}/cache/pear
install -d %{buildroot}%{_datadir}/pear/Archive
install -d %{buildroot}%{_datadir}/pear/Console
install -d %{buildroot}%{_datadir}/pear/Crypt
install -d %{buildroot}%{_datadir}/pear/HTML/Template
install -d %{buildroot}%{_datadir}/pear/HTTP
install -d %{buildroot}%{_datadir}/pear/Image
install -d %{buildroot}%{_datadir}/pear/Math
install -d %{buildroot}%{_datadir}/pear/Net
install -d %{buildroot}%{_datadir}/pear/PEAR
install -d %{buildroot}%{_datadir}/pear/Science
install -d %{buildroot}%{_datadir}/pear/Services
install -d %{buildroot}%{_datadir}/pear/Text
install -d %{buildroot}%{_datadir}/pear/XML
install -d %{buildroot}%{_datadir}/pear/docs
install -d %{buildroot}%{_datadir}/pear/data
install -d %{buildroot}%{_datadir}/pear/tests
install -d %{buildroot}%{_datadir}/pear/.registry
install -d %{buildroot}%{_datadir}/pear/packages

# PEAR
install -d %{buildroot}%{_datadir}/pear/OS
install -d %{buildroot}%{_datadir}/pear/PEAR/ChannelFile
install -d %{buildroot}%{_datadir}/pear/PEAR/Command
install -d %{buildroot}%{_datadir}/pear/PEAR/Downloader
install -d %{buildroot}%{_datadir}/pear/PEAR/Frontend
install -d %{buildroot}%{_datadir}/pear/PEAR/Installer/Role
install -d %{buildroot}%{_datadir}/pear/PEAR/PackageFile/Generator
install -d %{buildroot}%{_datadir}/pear/PEAR/PackageFile/Parser
install -d %{buildroot}%{_datadir}/pear/PEAR/PackageFile/v2
install -d %{buildroot}%{_datadir}/pear/PEAR/REST
install -d %{buildroot}%{_datadir}/pear/PEAR/Task/Postinstallscript
install -d %{buildroot}%{_datadir}/pear/PEAR/Task/Replace
install -d %{buildroot}%{_datadir}/pear/PEAR/Task/Unixeol
install -d %{buildroot}%{_datadir}/pear/PEAR/Task/Windowseol
install -d %{buildroot}%{_datadir}/pear/PEAR/Validator

install -m0755 PEAR-%{_PEAR_version}/scripts/pear.sh %{buildroot}%{_bindir}/pear
install -m0644 PEAR-%{_PEAR_version}/scripts/pearcmd.php %{buildroot}%{_datadir}/pear/
install -m0644 PEAR-%{_PEAR_version}/*.php %{buildroot}%{_datadir}/pear/
install -m0644 PEAR-%{_PEAR_version}/*.dtd %{buildroot}%{_datadir}/pear/
install -m0644 PEAR-%{_PEAR_version}/OS/*.php %{buildroot}%{_datadir}/pear/OS/
install -m0644 PEAR-%{_PEAR_version}/PEAR/*.php %{buildroot}%{_datadir}/pear/PEAR/
install -m0644 PEAR-%{_PEAR_version}/PEAR/ChannelFile/*.php %{buildroot}%{_datadir}/pear/PEAR/ChannelFile/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Command/*.php %{buildroot}%{_datadir}/pear/PEAR/Command/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Command/*.xml %{buildroot}%{_datadir}/pear/PEAR/Command/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Downloader/*.php %{buildroot}%{_datadir}/pear/PEAR/Downloader/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Frontend/CLI.php %{buildroot}%{_datadir}/pear/PEAR/Frontend/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Installer/*.php %{buildroot}%{_datadir}/pear/PEAR/Installer/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Installer/Role/*.php %{buildroot}%{_datadir}/pear/PEAR/Installer/Role/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Installer/Role/*.xml %{buildroot}%{_datadir}/pear/PEAR/Installer/Role/
install -m0644 PEAR-%{_PEAR_version}/PEAR/PackageFile/*.php %{buildroot}%{_datadir}/pear/PEAR/PackageFile/
install -m0644 PEAR-%{_PEAR_version}/PEAR/PackageFile/Generator/*.php %{buildroot}%{_datadir}/pear/PEAR/PackageFile/Generator/
install -m0644 PEAR-%{_PEAR_version}/PEAR/PackageFile/Parser/*.php %{buildroot}%{_datadir}/pear/PEAR/PackageFile/Parser/
install -m0644 PEAR-%{_PEAR_version}/PEAR/PackageFile/v2/*.php %{buildroot}%{_datadir}/pear/PEAR/PackageFile/v2/
install -m0644 PEAR-%{_PEAR_version}/PEAR/REST/*.php %{buildroot}%{_datadir}/pear/PEAR/REST/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Task/*.php  %{buildroot}%{_datadir}/pear/PEAR/Task/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Task/Postinstallscript/*.php %{buildroot}%{_datadir}/pear/PEAR/Task/Postinstallscript/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Task/Replace/*.php %{buildroot}%{_datadir}/pear/PEAR/Task/Replace/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Task/Unixeol/*.php %{buildroot}%{_datadir}/pear/PEAR/Task/Unixeol/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Task/Windowseol/*.php %{buildroot}%{_datadir}/pear/PEAR/Task/Windowseol/
install -m0644 PEAR-%{_PEAR_version}/PEAR/Validator/*.php %{buildroot}%{_datadir}/pear/PEAR/Validator/
install -m0644 PEAR.xml %{buildroot}%{_datadir}/pear/packages/PEAR.xml

# fix paths and such
find %{buildroot} -type f | xargs perl -pi -e "s|\@php_dir\@|%{_datadir}/pear|g"
find %{buildroot} -type f | xargs perl -pi -e "s|\@php_bin\@|%{_bindir}/php|g"
find %{buildroot} -type f | xargs perl -pi -e "s|\@pear_version\@|%{version}|g"

# Archive_Tar
install Archive_Tar-%{_Archive_Tar_version}/Archive/*.php %{buildroot}%{_datadir}/pear/Archive
install -m0644 Archive_Tar.xml %{buildroot}%{_datadir}/pear/packages/Archive_Tar.xml

# Console_Getopt
install Console_Getopt-%{_Console_Getopt_version}/Console/*.php %{buildroot}%{_datadir}/pear/Console
install -m0644 Console_Getopt.xml %{buildroot}%{_datadir}/pear/packages/Console_Getopt.xml

# Structures_Graph
install -d %{buildroot}%{_datadir}/pear/Structures/Graph/Manipulator
install Structures_Graph-%{_Structures_Graph_version}/Structures/*.php %{buildroot}%{_datadir}/pear/Structures
install Structures_Graph-%{_Structures_Graph_version}/Structures/Graph/*.php %{buildroot}%{_datadir}/pear/Structures/Graph/
install Structures_Graph-%{_Structures_Graph_version}/Structures/Graph/Manipulator/*.php %{buildroot}%{_datadir}/pear/Structures/Graph/Manipulator
install -m0644 Structures_Graph.xml %{buildroot}%{_datadir}/pear/packages/Structures_Graph.xml

# DB
install -d %{buildroot}%{_datadir}/pear/DB
install DB-%{_DB_version}/DB.php %{buildroot}%{_datadir}/pear/
install DB-%{_DB_version}/DB/*.php %{buildroot}%{_datadir}/pear/DB/
install -m0644 DB.xml %{buildroot}%{_datadir}/pear/packages/DB.xml

# Log
install -d %{buildroot}%{_datadir}/pear/Log
install Log-%{_Log_version}/*.php %{buildroot}%{_datadir}/pear
install Log-%{_Log_version}/Log/*.php %{buildroot}%{_datadir}/pear/Log
install -m0644 Log.xml %{buildroot}%{_datadir}/pear/packages/Log.xml

# Mail
install -d %{buildroot}%{_datadir}/pear/Mail
install Mail-%{_Mail_version}/*.php %{buildroot}%{_datadir}/pear/
install Mail-%{_Mail_version}/Mail/*.php %{buildroot}%{_datadir}/pear/Mail
install -m0644 Mail.xml %{buildroot}%{_datadir}/pear/packages/Mail.xml

# Mail_Mime
install Mail_Mime-%{_Mail_Mime_version}/*.php %{buildroot}%{_datadir}/pear/Mail/
install Mail_Mime-%{_Mail_Mime_version}/xmail.* %{buildroot}%{_datadir}/pear/Mail/
install -m0644 Mail_Mime.xml %{buildroot}%{_datadir}/pear/packages/Mail_Mime.xml

# Mail_mimeDecode
install Mail_mimeDecode-%{_Mail_mimeDecode_version}/*.php %{buildroot}%{_datadir}/pear/Mail/
install -m0644 Mail_mimeDecode.xml %{buildroot}%{_datadir}/pear/packages/Mail_mimeDecode.xml

# Net_SMTP
install Net_SMTP-%{_Net_SMTP_version}/SMTP.php %{buildroot}%{_datadir}/pear/Net
install -m0644 Net_SMTP.xml %{buildroot}%{_datadir}/pear/packages/Net_SMTP.xml

# Net_Socket
install Net_Socket-%{_Net_Socket_version}/*.php %{buildroot}%{_datadir}/pear/Net
install -m0644 Net_Socket.xml %{buildroot}%{_datadir}/pear/packages/Net_Socket.xml

# XML_Parser
install -d %{buildroot}%{_datadir}/pear/XML
install XML_Parser-%{_XML_Parser_version}/*.php %{buildroot}%{_datadir}/pear/XML
install -m0644 XML_Parser.xml %{buildroot}%{_datadir}/pear/packages/XML_Parser.xml

# XML_RPC
install -d %{buildroot}%{_datadir}/pear/XML/RPC
install XML_RPC-%{_XML_RPC_version}/RPC.php %{buildroot}%{_datadir}/pear/XML
install XML_RPC-%{_XML_RPC_version}/Server.php %{buildroot}%{_datadir}/pear/XML/RPC
install -m0644 XML_RPC.xml %{buildroot}%{_datadir}/pear/packages/XML_RPC.xml

cat > php.ini << EOF
open_basedir=
safe_mode=0
output_buffering=0
output_handler=0
magic_quotes_runtime=
extensions_dir=
session.save_path="."
EOF

PEAR_CMD="%{_bindir}/php -c ./php.ini -C -q -d include_path=%{buildroot}%{_datadir}/pear -d output_buffering=1 %{buildroot}%{_datadir}/pear/pearcmd.php"

# construct the ~/.pearrc file
${PEAR_CMD} config-set preferred_state stable
${PEAR_CMD} config-set bin_dir %{_bindir}
${PEAR_CMD} config-set php_dir %{_datadir}/pear
${PEAR_CMD} config-set doc_dir %{_datadir}/pear/docs
${PEAR_CMD} config-set data_dir %{_datadir}/pear/data
${PEAR_CMD} config-set test_dir %{_datadir}/pear/tests
${PEAR_CMD} config-set cache_dir %{_var}/cache/pear

# Turn generated conf into a global setting
grep -v '#' ~/.pearrc > pear.conf
php fixregistry.php pear.conf %{buildroot} 
install -m0644 pear.conf %{buildroot}%{_sysconfdir}/pear.conf

# cleanup 
rm -f %{buildroot}%{_datadir}/pear/.filemap
rm -f %{buildroot}%{_datadir}/pear/.lock

%post
if [ "$1" = "1" ]; then
    for p in %{_pear_packages}; do 
        if [ -f %{_datadir}/pear/packages/${p}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/${p}.xml
	fi
    done
fi
if [ "$1" = "2" ]; then
    for p in %{_pear_packages}; do 
        if [ -f %{_datadir}/pear/packages/${p}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/${p}.xml
	fi
    done
fi

# only do this if we have a working network
if /usr/sbin/hping -c 4 -p 80 --tcpexitcode pear.php.net >/dev/null 2>&1; then
    %{_bindir}/pear channel-update pear.php.net
else
    echo "You might want to run \"%{_bindir}/pear channel-update pear.php.net\" when your network works"
fi

%preun
if [ "$1" = "0" ]; then
    for p in %{_pear_packages}; do 
        if [ -f %{_datadir}/pear/packages/${p}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r ${p}
	fi
    done
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/pear.conf
%dir %{_sysconfdir}/pearkeys
%dir %{_datadir}/pear/Archive
%dir %{_datadir}/pear/Console
%dir %{_datadir}/pear/Crypt
%dir %{_datadir}/pear/HTML
%dir %{_datadir}/pear/HTML/Template
%dir %{_datadir}/pear/HTTP
%dir %{_datadir}/pear/Image
%dir %{_datadir}/pear/Math
%dir %{_datadir}/pear/Net
%dir %{_datadir}/pear/PEAR
%dir %{_datadir}/pear/Science
%dir %{_datadir}/pear/Services
%dir %{_datadir}/pear/Text
%dir %{_datadir}/pear/XML
%dir %{_datadir}/pear/docs
%dir %{_datadir}/pear/data
%dir %{_datadir}/pear/tests
%dir %{_datadir}/pear/packages
%dir %{_datadir}/pear/.registry
%dir %{_var}/cache/pear

# PEAR
%dir %{_datadir}/pear/OS
%dir %{_datadir}/pear/PEAR/ChannelFile
%dir %{_datadir}/pear/PEAR/Command
%dir %{_datadir}/pear/PEAR/Downloader
%dir %{_datadir}/pear/PEAR/Frontend
%dir %{_datadir}/pear/PEAR/Installer
%dir %{_datadir}/pear/PEAR/Installer/Role
%dir %{_datadir}/pear/PEAR/PackageFile
%dir %{_datadir}/pear/PEAR/PackageFile/Generator
%dir %{_datadir}/pear/PEAR/PackageFile/Parser
%dir %{_datadir}/pear/PEAR/PackageFile/v2
%dir %{_datadir}/pear/PEAR/REST
%dir %{_datadir}/pear/PEAR/Task
%dir %{_datadir}/pear/PEAR/Task/Postinstallscript
%dir %{_datadir}/pear/PEAR/Task/Replace
%dir %{_datadir}/pear/PEAR/Task/Unixeol
%dir %{_datadir}/pear/PEAR/Task/Windowseol
%dir %{_datadir}/pear/PEAR/Validator
%attr(755,root,root) %{_bindir}/pear
%{_datadir}/pear/*.dtd
%{_datadir}/pear/PEAR.php
%{_datadir}/pear/System.php
%{_datadir}/pear/pearcmd.php
%{_datadir}/pear/OS/*.php
%{_datadir}/pear/PEAR/*.php
%{_datadir}/pear/PEAR/ChannelFile/*.php
%{_datadir}/pear/PEAR/Command/*.php
%{_datadir}/pear/PEAR/Command/*.xml
%{_datadir}/pear/PEAR/Downloader/*.php
%{_datadir}/pear/PEAR/Frontend/*.php
%{_datadir}/pear/PEAR/Installer/*.php
%{_datadir}/pear/PEAR/Installer/Role/*.php
%{_datadir}/pear/PEAR/Installer/Role/*.xml
%{_datadir}/pear/PEAR/PackageFile/Generator/*.php
%{_datadir}/pear/PEAR/PackageFile/*.php
%{_datadir}/pear/PEAR/PackageFile/Parser/*.php
%{_datadir}/pear/PEAR/PackageFile/v2/*.php
%{_datadir}/pear/PEAR/REST/*.php
%{_datadir}/pear/PEAR/Task/Postinstallscript/*.php
%{_datadir}/pear/PEAR/Task/*.php
%{_datadir}/pear/PEAR/Task/Replace/*.php
%{_datadir}/pear/PEAR/Task/Unixeol/*.php
%{_datadir}/pear/PEAR/Task/Windowseol/*.php
%{_datadir}/pear/PEAR/Validator/*.php
%{_datadir}/pear/packages/PEAR.xml

# Archive_Tar
%doc Archive_Tar-%{_Archive_Tar_version}/docs/*
%{_datadir}/pear/Archive/*.php
%{_datadir}/pear/packages/Archive_Tar.xml

# Console_Getopt
%{_datadir}/pear/Console/*.php
%{_datadir}/pear/packages/Console_Getopt.xml

# Structures_Graph
%{_datadir}/pear/Structures/*.php
%{_datadir}/pear/Structures/Graph
%{_datadir}/pear/packages/Structures_Graph.xml

# DB
%doc DB-%{_DB_version}/{doc/*,tests}
%dir %{_datadir}/pear/DB
%{_datadir}/pear/DB.php
%{_datadir}/pear/DB/*.php
%{_datadir}/pear/packages/DB.xml

# Log
%doc Log-%{_Log_version}/{docs,tests}
%dir %{_datadir}/pear/Log
%{_datadir}/pear/Log.php
%{_datadir}/pear/Log/*.php
%{_datadir}/pear/packages/Log.xml

# Mail
%dir %{_datadir}/pear/Mail
%{_datadir}/pear/Mail.php
%{_datadir}/pear/Mail/RFC822.php
%{_datadir}/pear/Mail/mail.php
%{_datadir}/pear/Mail/null.php
%{_datadir}/pear/Mail/sendmail.php
%{_datadir}/pear/Mail/smtp.php
%{_datadir}/pear/packages/Mail.xml

# Mail_Mime
%{_datadir}/pear/Mail/mime.php
%{_datadir}/pear/Mail/mimePart.php
%{_datadir}/pear/Mail/xmail.dtd
%{_datadir}/pear/Mail/xmail.xsl
%{_datadir}/pear/packages/Mail_Mime.xml

# Mail_mimeDecode
%{_datadir}/pear/Mail/mimeDecode.php
%{_datadir}/pear/packages/Mail_mimeDecode.xml

# Net_SMTP
%{_datadir}/pear/Net/SMTP.php
%{_datadir}/pear/packages/Net_SMTP.xml

# Net_Socket
%{_datadir}/pear/Net/Socket.php
%{_datadir}/pear/packages/Net_Socket.xml

# XML_Parser
%doc XML_Parser-%{_XML_Parser_version}/tests/*
%{_datadir}/pear/XML/Parser.php
%{_datadir}/pear/packages/XML_Parser.xml

# XML_RPC
%{_datadir}/pear/XML/RPC.php
%{_datadir}/pear/XML/RPC/Server.php
%{_datadir}/pear/packages/XML_RPC.xml
