from peak.api import protocols, exceptions, PropertyName, NOT_GIVEN
from protocols import Interface, Attribute

__all__ = [
    'IConfigKey', 'IConfigurable', 'IConfigSource', 'IConfigurationRoot',
    'ISmartProperty', 'IRule', 'IPropertyMap', 'ISettingLoader',
    'IIniParser', 'ISettingParser', 'NullConfigRoot',
]


class IConfigKey(Interface):

    """Marker interface for configuration data keys

    Both 'PropertyName()' and 'Interface' objects are usable as
    configuration keys.  The common interface required is a subset of
    'Interface.IInterface' that's needed by property maps and EigenRegistry
    instances to use as dictionary keys.

    Configuration keys may be polymorphic at registration or lookup time.
    IOW, when looking up a configuration key, you can search multiple values
    that would imply the key being looked for.  And, when registering a value
    for a configuration key, the key can supply alternate keys that it should
    be registered under.  Thus, an 'IConfigKey' is never itself directly used
    as a key, only the values supplied by its 'registrationKeys()' and
    'lookupKeys()' methods are used.
    """

    def registrationKeys(depth=0):
        """Iterate over (key,depth) pairs to be used when registering"""

    def lookupKeys():
        """Iterate over keys that should be used for lookup"""








class IConfigSource(Interface):

    """Something that can be queried for configuration data"""

    def _getConfigData(forObj, configKey):

        """Return a value of 'configKey' for 'forObj' or 'NOT_FOUND'

        Note that 'configKey' is an 'IConfigKey' instance and may therefore be
        a 'PropertyName' or an 'Interface' object.

        Also note that 'binding.Component' implements this method by simply
        returning 'NOT_FOUND', and that is a perfectly acceptable
        implementation for many purposes."""


class IConfigurable(IConfigSource):

    """Object which can be configured with rules for configuration keys"""

    def registerProvider(configKey, ruleObj):

        """Register 'IRule' 'ruleObj' as a provider for 'configKey'

        'configKey' must be adaptable to 'IConfigKey'.  'ruleObj' will be
        registered as a provider of the specified key.

        If a provider has already been registered for the given key, the
        new provider will replace it, provided that it has not yet been
        used.  (If it has, 'AlreadyRead' should be raised.)

        If the key is an 'Interface' with bases (or any other type of
        configuration key that supports registering implied keys), the provider
        will also be registered for any keys implied by the supplied key,
        unless a provider was previously registered under the implied key.
        """





class IConfigurationRoot(IConfigSource):

    """A root component that acknowledges its configuration responsibilities"""

    def propertyNotFound(root,propertyName,forObj,default=NOT_GIVEN):
        """Property search failed"""

    def noMoreUtilities(root,configKey,forObj):
        """A utility search has completed"""

    def nameNotFound(root,name,forObj,bindName):
        """A (non-URL) component name was not found"""


class _NullConfigRoot(object):

    """Adapter to handle missing configuration root"""

    def propertyNotFound(self,root,propertyName,forObj,default=NOT_GIVEN):
        raise exceptions.InvalidRoot(
            "Root component %r does not implement 'IConfigurationRoot'"
            " (was looking up %s for %r)" % (root, propertyName, forObj)
        )

    def noMoreUtilities(self,root,configKey,forObj):
        raise exceptions.InvalidRoot(
            "Root component %r does not implement 'IConfigurationRoot'"
            " (was looking up %s for %r)" % (root, configKey, forObj)
        )

    def nameNotFound(self,root,name,forObj):
        raise exceptions.NameNotFound(
            remainingName = name, resolvedObj = root
        )

NullConfigRoot = _NullConfigRoot()





class IIniParser(Interface):

    """Parser object passed to 'ISettingParser' instances"""

    def add_setting(section, name, value, lineInfo):
        """Define a configuration rule for 'section'+'name' = value
        Note that when this method is called by the IIniParser itself,
        'section' already has the 'prefix' attribute added to it, and it
        is already formatted as a property prefix.  So, for a section like::

            [foo]
            bar = baz

        and a parser 'prefix' of '"some.prefix."', this method gets called
        with '("some.prefix.foo.", "bar", "baz", ...)'.
        """

    prefix = Attribute("""Prefix that should be added to all property names""")
    pMap       = Attribute("""IPropertyMap that the parser is loading""")
    globalDict = Attribute("""Globals dictionary used for eval()ing rules""")


class ISettingParser(Interface):

    """Handler for name=value settings in an .ini file section"""

    def __call__(parser, section, name, value, lineInfo):
        """Act on 'name' = 'value' in section 'section'

        'parser' is an 'IIniParser' for the file being parsed, and 'lineInfo'
        is a tuple of '(filename, lineNumber, lineContents)'.  Typically,
        a setting parser will perform some operation(s) on 'parser.pMap' in
        response to each setting it receives.

        If you want to use the standard parser's interpretation of the name
        and value, you can call 'parser.add_setting()', but be sure to
        provide compatible arguments, as 'add_setting()' expects its 'section'
        argument to be a valid, ready-to-use prefix for its 'name' argument.
        """


class IRule(Interface):

    """Rule to compute a property value for a target object"""

    def __call__(propertyMap, configKey, targetObject):

        """Retrieve 'configKey' for 'targetObject' or return 'NOT_FOUND'

        The rule object is allowed to call any 'IPropertyMap' methods on the
        'propertyMap' that is requesting computation of this rule.  It is
        also allowed to call 'config.getProperty()' relative to 'targetObject'
        or 'propertyMap'.

        What an IRule must *not* do, however, is return different results over
        time for the same input parameters.  If it cannot guarantee this
        algorithmically, it must cache its results keyed by the parameters it
        used, and not compute the results a second time."""
























class ISmartProperty(Interface):

    """An property value that itself should be treated as a rule

    Objects that implement this interface will have their 'computeProperty()'
    method called when they are used as the return value of an .ini-file
    property definition.  For example:

        [myapp.settings]
        foo.* = SomeRuleObject()

    If 'SomeRuleObject()' implements 'ISmartProperty', the return value of its
    'computeProperty()' method is returned as the value of any properties
    requested from the 'myapp.settings.foo.*' property namespace."""

    def computeProperty(propertyMap, name, prefix, suffix, targetObject):
        """Retrieve property 'rulePrefix+propertySuffix' from 'propertyMap'

        This is basically the same as 'IRule.__call__', except that the key
        must be a property name ('name'), and it is also broken into a 'prefix'
        for the name under which the rule was defined, and the 'suffix',
        if any."""



















class ISettingLoader(Interface):

    """Callable used to load configuration data"""

    def __call__(propertyMap, *args, **kw):
        """Load settings into 'propertyMap'

        Loading functions can require whatever arguments are useful or desired.
        The value of each "Load Settings From" config file entry will be
        interpreted as part of a call to the loader.  For example, this entry::

            [Load Settings From]
            mapping = importString('os.environ'), prefix='environ.*'

        will be interpereted as::

            loader(propertyMap, importString('os.environ'), prefix='environ.*')

        So it's up to the author of the loader to choose and document the
        arguments to be used in configuration files.

        However, one keyword argument which all 'ISettingLoader' functions
        must accept is 'includedFrom'.  This is an implementation-defined
        object which represents the state of the 'ISettingLoader' which is the
        caller.  Currently, this argument is only supplied by the default
        'config.loadConfigFile()' loader, and the value passed is a
        'ConfigReader' instance.
        """













class IPropertyMap(IConfigurable):

    """Specialized component for storing configuration data"""

    def setRule(propName, ruleObj):
        """Set rule for computing a property

        Note that if the specified property (or any more-specific form)
        has already been accessed, an 'AlreadyRead' exception results.

        'propName' may be a "wildcard", of the form '"part.of.a.name.*"'
        or '"*"' by itself in the degenerate case.  Wildcard rules are
        checked in most-specific-first order, after the non-wildcard name,
        and before the property's default."""

    def setDefault(propName, ruleObj):
        """Set 'IRule' 'defaultObj' as function to compute 'propName' default

        Note that if a default for the specified property has already been
        accessed, an 'AlreadyRead' exception results.  Also, if a value has
        already been set for the property, the default will be ignored.  The
        default will also be ignored if a rule exists for the same 'propName'
        (or parent wildcard thereof), unless the rule returns 'NOT_FOUND' or
        'NOT_GIVEN'.  Note: like values and unlike rules, defaults can *not*
        be registered for a wildcard 'propName'."""

    def setValue(propName, value):
        """Set property 'propName' to 'value'

        No wildcards allowed.  'AlreadyRead' is raised if the property
        has already been accessed for the target object."""

    def getValueFor(forObj, propName):
        """Return value of property for 'forObj' or return 'NOT_FOUND'"""







