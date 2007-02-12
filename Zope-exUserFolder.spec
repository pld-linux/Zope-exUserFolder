%define		fversion	%(echo %{version} |tr . _)
%define		zope_subname	exUserFolder
Summary:	Extensible User Folder
Summary(pl.UTF-8):	Rozszerzalne foldery użytkowników
Name:		Zope-%{zope_subname}
Version:	0.50.0
Release:	3
License:	GPL
Group:		Development/Tools
Source0:	http://dl.sourceforge.net/exuserfolder/%{zope_subname}-%{fversion}.tgz
# Source0-md5:	da885980aa9f7f8d19bf3f260242b2fe
Patch0:		%{name}-user_is_a_member.patch
URL:		http://www.zope.org/Members/TheJester/exUserFolder/
BuildRequires:	python
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	/usr/sbin/installzopeproduct
%pyrequires_eq	python-modules
Requires:	Zope
Requires:	Zope-CMF >= 1:1.4.2
Requires:	Zope-CMFPlone >= 2.0
Requires:	Zope-archetypes >= 1.2.5
Requires:	Zope-stripogram
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Extensible User Folder is a user folder that requires the
authentication of users to be removed from the storage of properties
for users.

%description -l pl.UTF-8
Rozszerzalne foldery użytkowników są folderami użytkowników
wymagającymi autoryzacji oddzielonej od kont użytkowników.

%prep
%setup -q -n %{zope_subname}
%patch0
find . -type f -name .cvsignore | xargs rm -rf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}

cp -af {Auth,Crypto,Group,Membership,Prop}Sources Extensions GroupSource I18N \
	PropertyEditor UserCache common dtml nullPlugin *.py *.gif version.txt \
	$RPM_BUILD_ROOT%{_datadir}/%{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}

# find $RPM_BUILD_ROOT -type f -name "*.py" -exec rm -rf {} \;;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/installzopeproduct %{_datadir}/%{name} %{zope_subname}
%service -q zope restart

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/installzopeproduct -d %{zope_subname}
	%service -q zope restart
fi

%files
%defattr(644,root,root,755)
%doc doc LICENSE CHANGES.txt
%{_datadir}/%{name}
