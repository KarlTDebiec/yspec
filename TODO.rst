To Do
=====

Present Tasks
-------------
- [✓] CLArgumentPlugin: Implement

Future Tasks
------------
- [ ] Start documentation
- [ ] Track argument access as well as origin
- [ ] Figure out how to offer multiple levels of help on CL
- [ ] YSpecConstructor: CL argument for plugin selection
- [ ] DefaultsPlugin: CL argument to read defaults from file
- [ ] DefaultsPlugin: Track path (for consistency)
- [ ] PresetsPlugin: CL argument to read available presets from file
- [ ] PresetsPlugin: Simplify to single loop?
- [ ] PresetsPlugin: Mutual exclusivity
- [ ] PresetsPlugin: Nested extension and inheritance
- [ ] PresetsPlugin: Reimplement help table; split out to general function
- [ ] SortPlugin: Track path (for consistency)
- [ ] WritePlugin: Implement; polish yaml_dump
- [ ] yaml_dump: Arguments to enable/disable annotation and set column number

Potential Future Tasks
----------------------
- [ ] ArgsPlugin: Implement; accept manual arguments for terminal
- [ ] Store argument origin (and usage) separately from comment (but similarly)
  by subclassing classes from ruamel
- [ ] ManualPlugin: CL argument to expand environment variables
- [ ] ManualPlugin: CL argument keep slices in final spec
- [ ] ManualPlugin: CL argument to prevent expansion of lists under "all"
- [ ] Consider splitting off indexed plugins; may be confusing if not needed

Minor Issues
------------
- Keys set to [] do not retain comment

Completed Tasks
---------------
- [✓] SortPlugin: Implement
- [✓] SortPlugin: Add some support for manual ordering
- [✓] PresetsPlugin: Set global preset manually
- [✓] PresetsPlugin: Reimplement support for preset inheritance and extension
- [✓] PresetsPlugin: Reimplement support for verbose preset output
- [✓] YSpecConstructor: Plugin order in help text

