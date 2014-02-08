%define	__noautoreq pear\\\\((PHPUnit.*|PEAR.*)\\\\)
%define Archive_Tar_version 1.3.9
%define Console_Getopt_version 1.3.1
%define Structures_Graph_version 1.0.4
%define XML_RPC_version 1.5.5
%define XML_Util_version 1.2.1

Summary:	PHP Extension and Application Repository
Name:		php-pear
Version:	1.9.4
Epoch:		1
Release:	6
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/PEAR/
Source0:	http://pear.php.net/get/PEAR-%{version}.tgz
Source1:	install-pear.php
Source2:	relocate.php
Source3:	strip.php
Source4:	LICENSE
Source5:	pear.script
Source10:	pear.sh
Source11:	pecl.sh
Source12:	peardev.sh
Source20:	http://pear.php.net/get/XML_RPC-%{XML_RPC_version}.tgz
Source21:	http://pear.php.net/get/Archive_Tar-%{Archive_Tar_version}.tgz
Source22:	http://pear.php.net/get/Console_Getopt-%{Console_Getopt_version}.tgz
Source23:	http://pear.php.net/get/Structures_Graph-%{Structures_Graph_version}.tgz
Source24:	http://pear.php.net/get/XML_Util-%{XML_Util_version}.tgz
Patch0:		PEAR-1.9.4-use-autoload.patch
BuildRequires:	php-cli
BuildRequires:	php-xml
Requires:	php-cli
Requires:	php-xml
Provides:	php-pear-Console_Getopt = %{Console_Getopt_version}
Provides:	php-pear-Archive_Tar = %{Archive_Tar_version}
Provides:	php-pear-Structures_Graph = %{Structures_Graph_version}
Provides:	php-pear-XML_RPC = %{XML_RPC_version}
Provides:	php-pear-XML_Util = %{XML_Util_version}
Obsoletes:	php-pear-XML_Util < %{XML_Util_version}
# the russian roulette fix - start
# this reduces breakage going from php-pear-5.2.x
Provides:	pear = %{epoch}:%{version}
Provides:	php-pear-PEAR = %{epoch}:%{version}
Provides:	php-pear-PEAR-Command = %{epoch}:%{version}
Provides:	php-pear-PEAR-Frontend_CLI = %{epoch}:%{version}
Provides:	php-pear-PEAR-OS = %{epoch}:%{version}
Obsoletes:	php-pear-PEAR
Obsoletes:	php-pear-PEAR-Command
Obsoletes:	php-pear-PEAR-Frontend_CLI
Obsoletes:	php-pear-PEAR-OS
# the russian roulette fix - end
Suggests:	php-pear-DB php-pear-Log php-pear-Mail php-pear-Mail_Mime php-pear-Mail_mimeDecode php-pear-Net_SMTP php-pear-Net_Socket php-pear-XML_Parser
BuildArch:	noarch

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

%patch0 -p1

%build

%install

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

%triggerpostun -- php-pear-XML-Util
# re-register extension unregistered during postun of obsoleted
# package php-pear-XML-Util
%{_bindir}/pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/XML_Util.xml >/dev/null || :

%files
%doc LICENSE README
%dir %{_sysconfdir}/pear
%config(noreplace) %{_sysconfdir}/pear.conf
%{_datadir}/pear
%{_bindir}/*
%dir %{_localstatedir}/cache/php-pear
%{_localstatedir}/lib/rpm/filetriggers/pear.*


%changelog
* Mon Apr 02 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.4-5
+ Revision: 788849
- the pecl script works now
- make the damn thing work

* Fri Mar 23 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1:1.9.4-4
+ Revision: 786274
- make sure that we really get rid of the dependencies we really don't want?\194?\164#"

* Thu Mar 22 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.4-3
+ Revision: 786020
- Archive_Tar-1.3.9
- various fixes

* Wed Nov 16 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.4-2
+ Revision: 730835
- various cleanups
- Archive_Tar-1.3.8
- XML_RPC-1.5.5

* Sun Jul 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.4-1
+ Revision: 690175
- 1.9.4

* Sat Jun 11 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.3-1
+ Revision: 684284
- 1.9.3

* Thu Apr 28 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.2-3
+ Revision: 660141
- wtf!?
- fix breakage

* Thu Apr 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.2-2
+ Revision: 651393
- Console_Getopt-1.3.1
- fix broken deps

* Mon Mar 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.9.2-1
+ Revision: 642443
- 1.9.2
- Console_Getopt-1.3.0
- Archive_Tar-1.3.7
- Structures_Graph-1.0.4
- XML_RPC-1.5.4

* Wed Oct 20 2010 Thierry Vignaud <tv@mandriva.org> 1:1.9.1-2mdv2011.0
+ Revision: 586991
- fix description

* Sat Aug 14 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.1-1mdv2011.0
+ Revision: 569593
- update to new version 1.9.1

* Mon Nov 09 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.0-6mdv2010.1
+ Revision: 463807
- use rpm filetriggers to register/unregister pear packages

* Fri Oct 02 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.0-5mdv2010.0
+ Revision: 452524
- fix dependencies for included packages

* Sat Sep 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.0-3mdv2010.0
+ Revision: 449423
- requires php-xml

* Sat Sep 26 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.0-2mdv2010.0
+ Revision: 449396
- fix dependencies

* Fri Sep 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 1:1.9.0-1mdv2010.0
+ Revision: 449239
- new version
- sync with fedora packaging:
 - use pear version number, not php one
 - split non-needed packages out
 - merge XML_Util
- package Net_Socket separatly

* Sat Jul 25 2009 Guillaume Rousse <guillomovitch@mandriva.org> 5.3.0-2mdv2010.0
+ Revision: 399769
- don't duplicate spec-helper job

  + Oden Eriksson <oeriksson@mandriva.com>
    - symbolic version bump
    - updated Net_SMTP-1.3.2 -> 1.3.3

* Mon Apr 20 2009 Raphaël Gertz <rapsys@mandriva.org> 5.2.9-2mdv2009.1
+ Revision: 368246
- Update PEAR to version 1.8.1
  Update pear Log to version 1.11.4
  Update pear Archive_Tar to version 1.3.3

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 5.2.9-1mdv2009.1
+ Revision: 341396
- symbolic version bump
- updated Net_SMTP-1.3.1 -> 1.3.2
- updated XML_Parser-1.3.1 -> 1.3.2

* Wed Dec 31 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.8-2mdv2009.1
+ Revision: 321795
- rebuild

* Tue Dec 09 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.8-1mdv2009.1
+ Revision: 312068
- symbolic version bump

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.7-1mdv2009.1
+ Revision: 310188
- symbolic version bump (5.2.7)
- updated Log-1.11.2 -> 1.11.3
- updated XML_Parser-1.2.8 -> 1.3.1

* Tue Sep 09 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-6mdv2009.0
+ Revision: 283096
- updated Log-1.11.1 -> 1.11.2

* Wed Aug 20 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-5mdv2009.0
+ Revision: 274195
- updated Log-1.11.0 -> 1.11.1
- updated Mail-1.1.14 -> 1.2.0b1

* Thu Jul 17 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-4mdv2009.0
+ Revision: 236799
- updated Net_SMTP-1.3.0 -> 1.3.1
- updated Log-1.10.1 -> 1.11.0
- updated Net_Socket-1.0.8 -> Net_Socket-1.0.9

* Sun May 18 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-3mdv2009.0
+ Revision: 208698
- updated PEAR-1.7.1 -> 1.7.2

* Sun May 04 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-2mdv2009.0
+ Revision: 201060
- updated Log-1.10.0 -> 1.10.1

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.6-1mdv2009.0
+ Revision: 200205
- symbolic version bump
- updated Net_SMTP-1.2.11 -> 1.3.0

* Sun Feb 17 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-4mdv2008.1
+ Revision: 169541
- use only upstream tarball format (.tgz)
- bump release
- updated Log-1.9.16 -> 1.10.0
- updated Net_SMTP-1.2.10 -> 1.2.11

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-3mdv2008.1
+ Revision: 162025
- updated Log-1.9.14 -> 1.9.16
- updated PEAR-1.6.2 -> 1.7.1

* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-2mdv2008.1
+ Revision: 141703
- updated Log-1.9.11 -> 1.9.14

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.5-1mdv2008.1
+ Revision: 107567
- fix build
- symbolic version bump
- updated DB-1.7.12 -> 1.7.13

* Tue Sep 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.4-1mdv2008.0
+ Revision: 84361
- cosmetic version bump
- updated PEAR-1.6.1 -> 1.6.2

* Fri Jun 29 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-5mdv2008.0
+ Revision: 45801
- updated DB-1.7.11 -> 1.7.12

* Sun Jun 24 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-4mdv2008.0
+ Revision: 43612
- updated PEAR-1.6.0 -> 1.6.1
- updated Mail_Mime-1.4.0 -> 1.5.2
- added Mail_mimeDecode-1.5.0

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-3mdv2008.0
+ Revision: 38417
- updated Console_Getopt-1.2.2 -> 1.2.3

* Fri Jun 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-2mdv2008.0
+ Revision: 37263
- updated PEAR-1.5.4 -> 1.6.0

* Mon Jun 04 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.3-1mdv2008.0
+ Revision: 35228
- cosmetic version bump

* Mon May 14 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-6mdv2008.0
+ Revision: 26624
- updated Log-1.9.10 -> 1.9.11

* Fri May 11 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-5mdv2008.0
+ Revision: 26255
- bundle Structures_Graph to avoid the warnings at install

* Tue May 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-4mdv2008.0
+ Revision: 25030
- updated PEAR-1.5.3 -> 1.5.4

* Mon May 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-3mdv2008.0
+ Revision: 24036
- update Mail_Mime 1.3.1 -> 1.4.0

* Fri May 04 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-2mdv2008.0
+ Revision: 22376
- actually add the Net_Socket-1.0.8 source
- updated Net_Socket-1.0.7 -> 1.0.8

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.2-1mdv2008.0
+ Revision: 21502
- cosmetic version bump

* Mon Apr 23 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-4mdv2008.0
+ Revision: 17304
- updated PEAR-1.5.2 -> 1.5.3

* Wed Apr 18 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-3mdv2008.0
+ Revision: 14669
- updated PEAR-1.5.0 -> 1.5.2
- updated Console_Getopt-1.2.1 -> 1.2.2
- updated DB-1.7.8 -> 1.7.11
- updated Net_SMTP-1.2.8 -> 1.2.10
- updated Net_Socket-1.0.6 -> 1.0.7
- dropped PHPUnit, it will be a stand alone package


* Fri Feb 09 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-2mdv2007.0
+ Revision: 118518
- use hping to determine if port 80 at pear.php.net can be reached

* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.1-1mdv2007.1
+ Revision: 117597
- cosmetic version bump

* Wed Feb 07 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-3mdv2007.1
+ Revision: 117306
- use a safe php.ini file to make it build on obscure systems

* Mon Feb 05 2007 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-2mdv2007.1
+ Revision: 116300
- PEAR-1.4.11 -> PEAR-1.5.0
- Archive_Tar-1.3.1 -> Archive_Tar-1.3.2
- Console_Getopt-1.2 -> Console_Getopt-1.2.1
- DB-1.7.6 -> DB-1.7.8
- Log-1.9.9 -> Log-1.9.10
- XML_Parser-1.2.7 -> XML_Parser-1.2.8

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 5.2.0-1mdv2007.1
+ Revision: 79259
- cosmetic rebuild
- updated Log-1.9.8 -> 1.9.9
- updated Mail-1.1.13 -> 1.1.14
- updated XML_RPC-1.5.0 -> 1.5.1
- Import php-pear

* Tue Sep 19 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.6-1mdv2007.0
- cosmetic rebuild

* Mon Sep 18 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-4mdv2007.0
- updated PEAR-1.4.10 -> 1.4.11
- updated Log-1.9.7 -> 1.9.8
- updated Mail-1.1.10 -> 1.1.13

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-3mdv2007.0
- updated PEAR-1.4.6 -> 1.4.10
- updated Log-1.9.3 -> 1.9.7
- updated Mail-1.1.9 -> 1.1.10
- updated Net_SMTP-1.2.7 -> 1.2.8
- updated XML_RPC-1.4.5 -> 1.5.0
- fix #23889

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-2mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.4-1mdk
- rebuilt for php-5.1.4

* Fri May 05 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.3-1mdk
- rebuilt for php-5.1.3

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.2-3mdk
- new group (Development/PHP)

* Thu Feb 02 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.2-2mdk
- new group (Development/PHP) and iurt rebuild
- updated XML_RPC-1.4.4 -> 1.4.5

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.2-1mdk
- rebuilt against php-5.1.2

* Mon Jan 09 2006 Oden Eriksson <oeriksson@mandriva.com> 5.1.1-2mdk
- updated PEAR-1.4.5 -> 1.4.6
- updated Log-1.9.2 -> 1.9.3

* Tue Nov 29 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.1-1mdk
- cosmetic rebuilt

* Sun Nov 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-1mdk
- updated PEAR-1.4.4 -> 1.4.5
- updated PHPUnit-1.3.1 -> 1.3.2

* Tue Nov 08 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC4.5mdk
- removed temporary requires, deps should be ok now

* Mon Nov 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC4.4mdk
- oops, some garbage slipped in the temporary requires

* Mon Nov 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC4.3mdk
- added temporary requires so that "rpmctl --move ..." won't take days...

* Mon Nov 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC4.2mdk
- fix some minor glitches

* Sun Nov 06 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0-0.RC4.1mdk
- updated PEAR-1.3.5 -> 1.4.4
- updated Log-1.8.7 -> 1.9.2
- updated XML_Parser-1.2.6 -> 1.2.7
- updated XML_RPC-1.4.1 -> 1.4.4

* Sat Sep 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-15mdk
- updated Mail-1.1.6 -> 1.1.9
- updated Net_SMTP-1.2.6 -> 1.2.7
- updated PHPUnit-1.2.3 -> 1.3.1
- updated XML_RPC-1.4.0 -> 1.4.1

* Wed Aug 31 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-14mdk
- update to XML_RPC 1.3.2 -> 1.4.0 (CAN-2005-2498)

* Fri Aug 26 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-13mdk
- obsolete the installed pear packages

* Wed Aug 10 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-12mdk
- rebuild

* Mon Aug 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.4-11mdk
- rebuilt to use new pear auto deps/reqs from pld

* Tue Aug 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-10mdk
- fix deps

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-9mdk
- fix deps

* Sun Jul 31 2005 Nicolas L�cureuil <neoclust@mandriva.org> 5.0.4-8mdk
- Add dos2unix as BuildRequires

* Fri Jul 22 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-7mdk
- fix deps again...

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-6mdk
- update Mail 1.1.4 -> 1.1.6
- update Mail_Mime 1.3.0 -> 1.3.1
- update XML_Parser 1.2.4 -> 1.2.6
- update XML_RPC 1.2.2 -> 1.3.3
- drop the XML_Parser.xml fix

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-5mdk
- argh!!!. it's much easier to bundle the deps..., so be it... it
  makes upgrades work better.
- fix a small bug in the XML_Parser.xml file that prevented 
  XML_Parser from being registered (P0)
- make it provide pear

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-4mdk
- fix the registration of the deps from this package because of
  circular dependencies (Stew Benedict)
- reworked the %%post and %%preun stuff, like in conectiva

* Wed Jul 20 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-3mdk
- fixed the %%trigger stuff (Buchan Milne)

* Wed Jul 20 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-2mdk
- reworked it some

* Tue Jul 19 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4-1mdk
- 5.0.4 (PLD import, sort of)

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11-1mdk
- 4.3.11

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 4.3.11-1mdk
- 4.3.11

* Mon Mar 21 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-3mdk
- use the %%mkrel macro

* Sun Jan 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-2mdk
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10-1mdk
- rebuild for 4.3.10

* Wed Nov 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9-1mdk
- 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8-1mdk
- 4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7-1mdk
- remove redundant provides

* Fri May 07 2004 Pascal Terjan <pterjan@mandrake.org> 4.3.6-1mdk
- php 4.3.6

* Fri Apr 23 2004 Pascal Terjan <pterjan@mandrake.org> 4.3.4-4mdk
- updated tarball
- require php-cli else /us/bin/pear won't run

